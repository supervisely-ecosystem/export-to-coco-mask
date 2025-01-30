import os
import supervisely as sly
import numpy as np
import ast
import json
from supervisely.io.fs import mkdir
from supervisely.annotation.json_geometries_map import GET_GEOMETRY_FROM_STR
from supervisely.geometry import bitmap, polygon, polyline, rectangle
from itertools import groupby
from distutils.util import strtobool
from dotenv import load_dotenv


if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))


def change_geometry_type(meta):
    new_classes = []

    for cls in meta.obj_classes:
        cls: sly.ObjClass

        if cls.geometry_type.geometry_name() in [
            geometry.geometry_name()
            for geometry in (polygon.Polygon, polyline.Polyline, rectangle.Rectangle)
        ]:
            new_classes.append(cls.clone(geometry_type=GET_GEOMETRY_FROM_STR("bitmap")))
        elif cls.geometry_type.geometry_name() == bitmap.Bitmap.geometry_name():
            new_classes.append(cls.clone())
        else:
            new_classes.append(cls.clone(geometry_type=GET_GEOMETRY_FROM_STR("polygon")))

    meta = meta.clone(obj_classes=sly.ObjClassCollection(new_classes))
    return meta


def convert_annotation(ann: sly.Annotation, dst_meta):
    new_labels = []
    for lbl in ann.labels:
        new_cls = dst_meta.obj_classes.get(lbl.obj_class.name)
        if lbl.obj_class.geometry_type == new_cls.geometry_type:
            new_labels.append(lbl)
        else:
            converted_labels = lbl.convert(new_cls)
            new_labels.extend(converted_labels)
    return ann.clone(labels=new_labels)


def get_categories_map_from_meta(meta):
    obj_classes = meta.obj_classes
    categories_mapping = {}
    for idx, obj_class in enumerate(obj_classes):
        categories_mapping[obj_class.name] = idx + 1
    return categories_mapping


def get_categories_from_meta(meta):
    obj_classes = meta.obj_classes
    categories = []
    for idx, obj_class in enumerate(obj_classes):
        categories.append(
            dict(
                supercategory=obj_class.name,
                id=idx + 1,  # supercategory id
                name=obj_class.name,
            )
        )
    return categories


def coco_segmentation(segmentation):
    segmentation = [float(coord) for sublist in segmentation for coord in sublist]
    return segmentation


def extend_mask_up_to_image(binary_mask, image_shape, origin):
    y, x = origin.col, origin.row
    new_mask = np.zeros(image_shape, dtype=binary_mask.dtype)
    new_mask[x : x + binary_mask.shape[0], y : y + binary_mask.shape[1]] = binary_mask
    return new_mask


def coco_segmentation_rle(segmentation):
    binary_mask = np.asfortranarray(segmentation)
    rle = {"counts": [], "size": list(binary_mask.shape)}
    counts = rle.get("counts")
    for i, (value, elements) in enumerate(groupby(binary_mask.ravel(order="F"))):
        if i == 0 and value == 1:
            counts.append(0)
        counts.append(len(list(elements)))
    return rle


def coco_bbox(bbox):
    bbox = [float(coord) for sublist in bbox for coord in sublist]
    x, y, max_x, max_y = bbox
    width = max_x - x
    height = max_y - y
    bbox = (x, y, width, height)
    return bbox


def create_coco_dataset(coco_dataset_dir):
    mkdir(coco_dataset_dir)
    img_dir = os.path.join(coco_dataset_dir, "images")
    mkdir(img_dir)
    ann_dir = os.path.join(coco_dataset_dir, "annotations")
    mkdir(ann_dir)
    return img_dir, ann_dir


def create_coco_annotation(
    meta,
    categories_mapping,
    dataset,
    user_name,
    image_infos,
    anns,
    label_id,
    coco_ann,
    progress,
):
    if len(coco_ann) == 0:
        coco_ann = dict(
            info=dict(
                description=dataset.description,
                url="None",
                version=str(1.0),
                year=int(dataset.created_at[:4]),
                contributor=user_name,
                date_created=dataset.created_at,
            ),
            licenses=[dict(url="None", id=0, name="None")],
            images=[
                # license, url, file_name, height, width, date_captured, id
            ],
            # type="instances",
            annotations=[
                # segmentation, area, iscrowd, image_id, bbox, category_id, id
            ],
            categories=get_categories_from_meta(meta),  # supercategory, id, name
        )

    for image_info, ann in zip(image_infos, anns):
        coco_ann["images"].append(
            dict(
                license="None",
                file_name=image_info.name,
                url="None",  # image_info.full_storage_url,  # coco_url, flickr_url
                height=image_info.height,
                width=image_info.width,
                date_captured=image_info.created_at,
                id=image_info.id,
            )
        )

        for label in ann.labels:
            if label.geometry.geometry_name() == bitmap.Bitmap.geometry_name():
                segmentation = extend_mask_up_to_image(
                    label.geometry.data,
                    (image_info.height, image_info.width),
                    label.geometry.origin,
                )
                segmentation = coco_segmentation_rle(segmentation)
            else:
                segmentation = label.geometry.to_json()["points"]["exterior"]
                segmentation = [coco_segmentation(segmentation)]

            bbox = label.geometry.to_bbox().to_json()["points"]["exterior"]
            bbox = coco_bbox(bbox)

            label_id += 1
            coco_ann["annotations"].append(
                dict(
                    segmentation=segmentation,
                    area=label.geometry.area,
                    iscrowd=0,
                    image_id=image_info.id,
                    bbox=bbox,
                    category_id=categories_mapping[label.obj_class.name],
                    id=label_id,
                )
            )
        progress.iter_done_report()
    return coco_ann, label_id


class MyExport(sly.app.Export):
    def process(self, context: sly.app.Export.Context):
        api = sly.Api.from_env()

        user_name = "Supervisely"
        project = api.project.get_info_by_id(context.project_id)
        meta_json = api.project.get_meta(context.project_id)
        meta = sly.ProjectMeta.from_json(meta_json)

        selected_output = os.environ["modal.state.selectedOutput"]
        selected_filter = os.environ["modal.state.selectedFilter"]
        all_datasets = bool(strtobool(os.getenv("modal.state.allDatasets")))
        selected_datasets = ast.literal_eval(os.environ["modal.state.datasets"])

        storage_dir = os.path.join(sly.app.get_data_dir(), "storage_dir")
        mkdir(storage_dir, True)

        full_archive_name = f"{project.id}_{project.name}"
        coco_base_dir = os.path.join(storage_dir, full_archive_name)
        mkdir(coco_base_dir)

        new_meta = change_geometry_type(meta)
        categories_mapping = get_categories_map_from_meta(new_meta)

        if not all_datasets and not selected_datasets:
            all_datasets = True

        if all_datasets:
            datasets = list(api.dataset.get_list(context.project_id))
        else:
            datasets = [api.dataset.get_info_by_id(dataset_id) for dataset_id in selected_datasets]
        label_id = 0

        for dataset in datasets:
            sly.logger.info(f"processing {dataset.name}...")
            coco_dataset_dir = os.path.join(coco_base_dir, dataset.name)

            coco_ann = {}
            images = api.image.get_list(dataset.id)

            if selected_filter == "annotated":
                images = [
                    image for image in images if image.labels_count > 0 or len(image.tags) > 0
                ]

            if len(images) == 0:
                continue

            img_dir, ann_dir = create_coco_dataset(coco_dataset_dir)

            ds_progress = sly.Progress(
                f"Converting dataset: {dataset.name}",
                total_cnt=len(images),
                min_report_percent=5,
            )
            
            image_ids = [image_info.id for image_info in images]
            loop = sly.utils.get_or_create_event_loop()
            if selected_output == "images":
                image_paths = [os.path.join(img_dir, image_info.name) for image_info in images]                
                loop.run_until_complete(api.image.download_paths_async(image_ids, image_paths))

            ann_infos = loop.run_until_complete(api.annotation.download_bulk_async(dataset.id, image_ids))
            anns = [sly.Annotation.from_json(x.annotation, meta) for x in ann_infos]
            anns = [convert_annotation(ann, new_meta) for ann in anns]
            coco_ann, label_id = create_coco_annotation(
                meta,
                categories_mapping,
                dataset,
                user_name,
                images,
                anns,
                label_id,
                coco_ann,
                ds_progress,
            )
            with open(os.path.join(ann_dir, "instances.json"), "w") as file:
                json.dump(coco_ann, file)

            sly.logger.info(f"dataset {dataset.name} processed!")

        return coco_base_dir


app = MyExport()
app.run()
