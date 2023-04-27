<div align="center" markdown>
<img src=""/>

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

The application converts the project in [Superviselyformat](https://docs.supervise.ly/data-organization/00_ann_format_navi) to [COCO format](https://cocodataset.org/#home) as a **downloadable .tar archive**

Application key points:

- Supports only **instances.json** from **COCO** format
- Only bitmaps, polygons, polylines, and rectangles will be saved as masks with RLE. Other types will be saved as polygons.

# How to Use

1. Run app [Export to COCO mask](https://ecosystem.supervise.ly/apps/export-to-coco-mask) from the context menu of **Images Project**:

<img src="" width="100%"/>

1. Select options in the modal window and press the **RUN** button

<div align="center" markdown>
  <img src="" width="70%"/>
</div>

# Results

After running the application, you will be redirected to the `Tasks` page. Once application processing has finished, your link for downloading will be available. Click on the `file name` to download it.

<img src=""/>

You can also find your converted project in  
`Team Files` -> `tmp > supervisely > export > taskId` -> `<taskId>_<projectName>.tar`

<img src=""/>
