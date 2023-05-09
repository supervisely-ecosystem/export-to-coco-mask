<div align="center" markdown>
<img src="https://user-images.githubusercontent.com/57998637/234995761-64275f3d-77c6-4ac8-8c05-762cc6f8ad56.png"/>

# Export to COCO mask

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Use">How To Use</a> •
  <a href="#Results">Results</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/export-to-coco-mask)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/export-to-coco-mask)
[![views](https://app.supervise.ly/img/badges/views/supervisely-ecosystem/export-to-coco-mask.png)](https://supervise.ly)
[![runs](https://app.supervise.ly/img/badges/runs/supervisely-ecosystem/export-to-coco-mask.png)](https://supervise.ly)

</div>

# Overview

When it comes to annotating objects with complex shapes and structures, using masks can be a more accurate and efficient method compared to other techniques like bounding boxes or polygons. Masks allow you to precisely outline the object's shape, including any holes or gaps within it, which is not possible with polygons. Additionally, masks can help in scenarios where objects may overlap or intersect with one another, making it easier to separate and distinguish them. Using masks can provide a more robust and accurate annotation process for complex objects in image analysis tasks.

The application converts the project from [Supervisely format](https://docs.supervise.ly/data-organization/00_ann_format_navi) to [COCO format](https://cocodataset.org/#format-data) as masks with uncompressed RLE to preserve holes in annotations.

You can also learn about the COCO format in detail in the [article](https://www.immersivelimit.com/tutorials/create-coco-annotations-from-scratch).

⚠️ Only bitmaps, polygons, polylines, and rectangles will be saved as masks. Other types will be saved as polygons.

# How to Use

1. Run app [Export to COCO mask](https://ecosystem.supervise.ly/apps/export-to-coco-mask) from:

   - the context menu of the **Images Project**

      <div align="left" markdown>
        <img width="454" alt="menu" src="https://user-images.githubusercontent.com/57998637/234990671-1844c7ef-e1ce-4f8a-abca-4f5f5b74dfa8.png">
      </div>

   - the personal page of the app in Ecosystem

      <div align="left" markdown>
        <img width="394" alt="personal_page" src="">
      </div>

2. Select options in the modal window and press the **RUN** button

    <div align="left" makdown>
         <img width="394" alt="modal_window" src="https://user-images.githubusercontent.com/57998637/234990668-b552d09a-1ff9-4e53-814e-08d148ae3d41.png"></img>
    </div>

# Results

After running the application, you will be redirected to the `Tasks` page. Once application processing has finished, your link for downloading will be available. Click on the `file name` to download it.

<img width="422" alt="tasks_page" src="">

You can also find your converted project in [Team Files](https://app.supervise.ly/files/)

`tmp > supervisely > export > Export to COCO mask > Task Id` -> `<taskId>_<projectName>.tar`

<img width="422" alt="team_files" src="https://user-images.githubusercontent.com/57998637/234997034-ac247bac-7606-4b98-a950-429ff868e25e.png">
