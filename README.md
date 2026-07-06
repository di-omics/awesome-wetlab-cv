# Awesome Wet-Lab Computer Vision [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> Curated computer vision for the **wet lab** and **autonomous science**: the models, trackers, and robot stacks that turn a microscope or a liquid handler into something that sees, decides, and acts.

![Last updated](https://img.shields.io/badge/last%20updated-2026--07--06-blue) ![License: CC0-1.0](https://img.shields.io/badge/license-CC0--1.0-lightgrey)

## Why this list

CV for autonomous wet labs is scattered: bio-image segmentation lives in one world, real-time detection in another, robotics in a third, and almost nothing connects them to *execution*. This list maps the field, biased toward what plugs into a real lab: eval-first pipelines, models you can compose (`detect -> track -> verify -> act`), and the tacit steps a protocol omits. Opinionated on purpose. ⭐ marks my picks for a lab that runs itself.

Maintained by [Di Hu](https://github.com/di-omics).

## Contents

- [Foundation Models & Backbones](#foundation-models--backbones)
- [Real-Time Detection](#real-time-detection)
- [Bio-Image Segmentation](#bio-image-segmentation)
- [Cell & Object Tracking](#cell--object-tracking)
- [Vision-Language Models](#vision-language-models)
- [Vision-Language-Action & Lab Robotics](#vision-language-action--lab-robotics)
- [Eval, Annotation & Composition](#eval-annotation--composition)
- [Datasets](#datasets)
- [Reproductive & Embryo CV](#reproductive--embryo-cv)
- [Key Papers & Surveys](#key-papers--surveys)
- [Contributing](#contributing)
- [License](#license)

> ⭐ = my pick: load-bearing for an eval-first autonomous-lab stack.

## Foundation Models & Backbones

- ⭐ [facebookresearch/sam2](https://github.com/facebookresearch/sam2) - Segment Anything 2: promptable image + **video** segmentation with memory; the tracking backbone for a lab scene. Apache-2.0.
- [facebookresearch/segment-anything](https://github.com/facebookresearch/segment-anything) - the original SAM; still the cleanest promptable-mask baseline. Apache-2.0.
- ⭐ [facebookresearch/dinov2](https://github.com/facebookresearch/dinov2) - self-supervised ViT features that transfer to microscopy without labels; strong frozen backbone for few-shot lab tasks. Apache-2.0.
- [facebookresearch/dino](https://github.com/facebookresearch/dino) - the self-distillation method DINOv2 grew from; attention maps that segment for free. Apache-2.0.
- [facebookresearch/detectron2](https://github.com/facebookresearch/detectron2) - batteries-included detection/segmentation framework; a solid harness when you need Mask R-CNN done right. Apache-2.0.
- [IDEA-Research/GroundingDINO](https://github.com/IDEA-Research/GroundingDINO) - open-vocabulary detection from text prompts; point at "colony" or "meniscus" without a trained head. Apache-2.0.
- [IDEA-Research/Grounded-Segment-Anything](https://github.com/IDEA-Research/Grounded-Segment-Anything) - GroundingDINO + SAM: text to box to mask, zero-shot. Apache-2.0.
- [mlfoundations/open_clip](https://github.com/mlfoundations/open_clip) - open reproduction of CLIP; the go-to for image-text embeddings you can actually retrain.
- [openai/CLIP](https://github.com/openai/CLIP) - the original contrastive image-text model; still a useful zero-shot classifier. MIT.

## Real-Time Detection

- ⭐ [roboflow/rf-detr](https://github.com/roboflow/rf-detr) - real-time DETR from Roboflow; transformer accuracy at YOLO speed, **Apache-2.0** (no AGPL strings). My default when detection ships into a product.
- [lyuwenyu/RT-DETR](https://github.com/lyuwenyu/RT-DETR) - the original real-time DETR; end-to-end, NMS-free. Apache-2.0.
- [ultralytics/ultralytics](https://github.com/ultralytics/ultralytics) - YOLO11 and friends; fastest path to a working detector, but **AGPL-3.0** - license-check before shipping.
- [THU-MIG/yolov10](https://github.com/THU-MIG/yolov10) - NMS-free YOLO, lower latency. AGPL-3.0.
- [WongKinYiu/yolov9](https://github.com/WongKinYiu/yolov9) - programmable gradient information; strong accuracy. GPL-3.0.
- [meituan/YOLOv6](https://github.com/meituan/YOLOv6) - industrial-tuned single-stage detector. GPL-3.0.

## Bio-Image Segmentation

- ⭐ [MouseLand/cellpose](https://github.com/MouseLand/cellpose) - generalist cell/nucleus segmentation that works out-of-the-box across modalities; the wet-lab workhorse. BSD-3.
- [stardist/stardist](https://github.com/stardist/stardist) - star-convex polygons for crowded nuclei; where Cellpose struggles on dense DAPI. BSD-3.
- ⭐ [computational-cell-analytics/micro-sam](https://github.com/computational-cell-analytics/micro-sam) - SAM fine-tuned + interactive for microscopy; annotate and segment in napari. MIT.
- [vanvalenlab/cellSAM](https://github.com/vanvalenlab/cellSAM) - a foundation model for universal cell segmentation. Apache-2.0.
- [vanvalenlab/deepcell-tf](https://github.com/vanvalenlab/deepcell-tf) - DeepCell / Mesmer for tissue and whole-cell segmentation. Apache-2.0.
- [constantinpape/torch-em](https://github.com/constantinpape/torch-em) - PyTorch training utilities purpose-built for bio-image segmentation (the engine under micro-sam). MIT.
- [juglab/n2v](https://github.com/juglab/n2v) - Noise2Void self-supervised denoising; clean up low-SNR frames before you segment.

## Cell & Object Tracking

- ⭐ [royerlab/ultrack](https://github.com/royerlab/ultrack) - large-scale cell tracking via segmentation-hypothesis selection; scales to crowded, dividing populations. BSD-3.
- ⭐ [weigertlab/trackastra](https://github.com/weigertlab/trackastra) - transformer-based cell tracking that links existing segmentations, no tuning. BSD-3.
- [trackmate-sc/TrackMate](https://github.com/trackmate-sc/TrackMate) - the Fiji tracking standard; GUI + scriptable, huge ecosystem. GPL-3.0.
- [quantumjot/btrack](https://github.com/quantumjot/btrack) - Bayesian multi-object tracking with lineage trees. MIT.
- [soft-matter/trackpy](https://github.com/soft-matter/trackpy) - classic particle tracking (Crocker-Grier); still the right tool for beads and diffusing spots.

## Vision-Language Models

- [QwenLM/Qwen3-VL](https://github.com/QwenLM/Qwen3-VL) - strong open VLM with grounding + OCR; reads plate labels and instrument screens well. Apache-2.0.
- [OpenGVLab/InternVL](https://github.com/OpenGVLab/InternVL) - open multimodal model family competitive on fine-grained visual tasks. MIT.
- [haotian-liu/LLaVA](https://github.com/haotian-liu/LLaVA) - the reference open VLM recipe; easy to fine-tune on lab imagery. Apache-2.0.

## Vision-Language-Action & Lab Robotics

- ⭐ [huggingface/lerobot](https://github.com/huggingface/lerobot) - the open stack for real-world robot learning: datasets, policies, sim; where lab manipulation is converging. Apache-2.0.
- [openvla/openvla](https://github.com/openvla/openvla) - open 7B vision-language-action model; language + camera in, robot actions out. MIT.
- [Physical-Intelligence/openpi](https://github.com/Physical-Intelligence/openpi) - open π0-family VLA policies for dexterous manipulation. Apache-2.0.
- [google-deepmind/open_x_embodiment](https://github.com/google-deepmind/open_x_embodiment) - the cross-embodiment robot dataset + RT-X models; the ImageNet moment for robot data. Apache-2.0.
- ⭐ [PyLabRobot/pylabrobot](https://github.com/PyLabRobot/pylabrobot) - hardware-agnostic Python for liquid handlers and lab devices; the execution layer CV should drive. MIT.
- [Opentrons/opentrons](https://github.com/Opentrons/opentrons) - open liquid-handling robots + Python protocol API. Apache-2.0.

## Eval, Annotation & Composition

- ⭐ [roboflow/supervision](https://github.com/roboflow/supervision) - the glue: compose detect + segment + track + zones/line-counters into one pipeline. MIT.
- ⭐ [voxel51/fiftyone](https://github.com/voxel51/fiftyone) - dataset + model **evaluation** you can see; find failure modes before they reach the bench. Apache-2.0.
- [napari/napari](https://github.com/napari/napari) - n-dimensional image viewer; the annotation + inspection hub for microscopy in Python. BSD-3.
- [HumanSignal/label-studio](https://github.com/HumanSignal/label-studio) - flexible multi-type annotation for building lab-specific train/eval sets. Apache-2.0.
- [cocodataset/cocoapi](https://github.com/cocodataset/cocoapi) - pycocotools: the reference mAP / AP implementation for detection eval.

## Datasets

- [sartorius-research/LIVECell](https://github.com/sartorius-research/LIVECell) - large label-dense phase-contrast dataset for single-cell segmentation. Code + data.
- [TissueNet (datasets.deepcell.org)](https://datasets.deepcell.org/) - multiplexed tissue imaging with whole-cell annotations; the DeepCell/Mesmer benchmark.
- [Cell Tracking Challenge](https://celltrackingchallenge.net/) - the standard 2D/3D+t benchmark and metrics for cell segmentation and tracking.
- [SA-V (Segment Anything Video)](https://ai.meta.com/datasets/segment-anything-video/) - the large video segmentation dataset behind SAM 2.

## Reproductive & Embryo CV

The clinical leaders here (iDAScore, KIDScore) are closed. My POV: **assemble it from the open stack**. A detector for the embryo/blastomere ROI, SAM 2 for the mask, Ultrack or Trackastra for cleavage-division lineage over the time-lapse, evaluated with FiftyOne. The open literature is enough to reproduce the signal.

- [Khosravi et al., 2019 - STORK](https://doi.org/10.1038/s41746-019-0096-y) - deep learning for robust blastocyst assessment/selection (*npj Digital Medicine*).
- [Berntsen et al., 2022 - iDAScore v1.0](https://doi.org/10.1371/journal.pone.0262661) - generalizable embryo selection from time-lapse image sequences (*PLOS ONE*).

## Key Papers & Surveys

- [Segment Anything](https://arxiv.org/abs/2304.02643) (Kirillov et al., 2023) - the promptable-segmentation foundation.
- [SAM 2: Segment Anything in Images and Videos](https://arxiv.org/abs/2408.00714) (Ravi et al., 2024) - memory-based video segmentation.
- [DINOv2: Learning Robust Visual Features without Supervision](https://arxiv.org/abs/2304.07193) (Oquab et al., 2023).
- [Cell Detection with Star-Convex Polygons](https://arxiv.org/abs/1806.03535) (Schmidt et al., 2018) - StarDist.
- [DETRs Beat YOLOs on Real-time Object Detection](https://arxiv.org/abs/2304.08069) (Zhao et al., 2023) - RT-DETR.
- [Trackastra: Transformer-based cell tracking for live-cell microscopy](https://arxiv.org/abs/2405.15700) (Gallusser & Weigert, 2024).
- [OpenVLA: An Open-Source Vision-Language-Action Model](https://arxiv.org/abs/2406.09246) (Kim et al., 2024).
- [Cellpose: a generalist algorithm for cellular segmentation](https://doi.org/10.1038/s41592-020-01018-x) (Stringer et al., 2021, *Nature Methods*).
- [Cellpose 2.0: how to train your own model](https://doi.org/10.1038/s41592-022-01663-4) (Pachitariu & Stringer, 2022, *Nature Methods*).
- [Deep learning for cellular image analysis](https://doi.org/10.1038/s41592-019-0403-1) (Moen et al., 2019, *Nature Methods*) - the field survey.
- [An autonomous laboratory for the accelerated synthesis of inorganic materials](https://doi.org/10.1038/s41586-023-06734-w) (Szymanski et al., 2023, *Nature*) - the A-Lab; what closed-loop autonomous science looks like.

## Contributing

Contributions welcome, see [CONTRIBUTING.md](CONTRIBUTING.md). One hard rule: **every link must resolve to the real, canonical source.** Dead or guessed links get rejected.

## License

[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](https://creativecommons.org/publicdomain/zero/1.0/)

To the extent possible under law, the maintainers have waived all copyright and related rights to this work under [CC0 1.0](LICENSE).
