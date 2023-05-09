<div align="center" markdown>
<img src="https://github.com/supervisely-ecosystem/export-to-coco-mask/assets/119248312/ead97f45-1f99-4198-844c-104e004f52d6"/>

# Export to COCO mask

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#Preparation">Preparation</a> •
  <a href="#How-to-Run">How to Run</a> •
  <a href="#How-to-Use">How to Use</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/export-to-coco-mask)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/export-to-coco-mask)
[![views](https://app.supervise.ly/img/badges/views/supervisely-ecosystem/export-to-coco-mask.png)](https://supervise.ly)
[![runs](https://app.supervise.ly/img/badges/runs/supervisely-ecosystem/export-to-coco-mask.png)](https://supervise.ly)

</div>

# Overview

The application converts the project from [Supervisely format](https://docs.supervise.ly/data-organization/00_ann_format_navi) to [COCO format](https://cocodataset.org/#format-data) as masks with uncompressed RLE to preserve holes in annotations.

When it comes to annotating objects with complex shapes and structures, using masks can be a more accurate and efficient method compared to other techniques like bounding boxes or polygons. Masks allow you to precisely outline the object's shape, including any holes or gaps within it, which is not possible with polygons. Additionally, masks can help in scenarios where objects may overlap or intersect with one another, making it easier to separate and distinguish them. Using masks can provide a more robust and accurate annotation process for complex objects in image analysis tasks.

You can also learn about the COCO format in detail in the [article](https://www.immersivelimit.com/tutorials/create-coco-annotations-from-scratch).

⚠️ **Only bitmaps, polygons, polylines, and rectangles will be saved as masks. Other types will be saved as polygons.**

# How to Run 

1. Add app to your team from [Ecosystem](https://ecosystem.supervise.ly/apps/export-to-coco-mask) if it is not there.

2. Open context menu of project -> `Download as` -> `Export to COCO mask` 
<img src="XXX" />

You can also run the application from the Ecosystem.
<img src="XXX" />

# How to Use

App creates task in `workspace tasks` list. Once app is finished, you will see download link to resulting tar archive. 

<img src="XXX" />

Resulting archive is saved in : 

`Current Team` -> `Files` -> `/tmp/supervisely/export/Export to COCO mask/<task_id>/<project_id>_<project_name>.tar`. 

For example our file path is the following: 

`/tmp/supervisely/export/Export to COCO mask/33518/tomato-slices.tar`.

