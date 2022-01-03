# Diagnostics of Lewy body diseases in prodromal stage based on multimodal data analysis (decision support system)

## Repository

This repository contains references to submodules of the Lewy Body Diseases (LBD) analysis system (LBD decision support system) that are stored in separate GitHub repositories. The system is composed of the following:
1. web-application: https://github.com/BDALab/lbd_analysis_tool
2. micro-services
   1. featurizer services
      1. client: https://github.com/BDALab/featurizer-api-client
      2. server: https://github.com/BDALab/featurizer-api
   2. predictor services
      1. client: https://github.com/BDALab/predictor-api-client
      2. server: https://github.com/BDALab/predictor-api

## Project description

Lewy body diseases (LBDs) is a term describing a group of neurodegenerative disorders (i.e. dementia with Lewy bodies and Parkinson’s disease) characterized by pathophysiological process of alfa-synuclein accumulation in specific brain regions leading to the formation of Lewy bodies inside neurons and resulting in cell death. LBDs are progressing slowly and are usually diagnosed when the neurodegenerative process has reached severe degree in which most of the targeted neurons have already been damaged. Identification of LBDs at an early stage is crucial for development of disease-modifying treatment since the neurodegeneration may be possibly stopped or treated at the onset. In the frame of this project we are going to employ a complex multimodal analysis in order to identify prodromal biomarkers of LBDs and describe underlying pathophysiological processes. Consequently, this knowledge will be used to introduce a new machine-learning based decision support system that will help to assess, diagnose and monitor LBDs.

The main goal of this multidisciplinary project is to extend the knowledge in the field of LBDs diagnosis and introduce novel non-invasive methods such as acoustic analysis of speech, MRI, EEG and actigraphy during sleep as potential diagnostic biomarkers that will enhance sensitivity and specificity of prodromal Parkinson’s disease (PD) and dementia with Lewy bodies (DLB) diagnosis, and enhance accuracy of calculated individual risk scores for diagnosis of probable prodromal PD/DLB. In addition, we will develop a new open-source decision support system that will help to assess, diagnose and monitor patients with LBDs, even in the prodromal stage of the diseases. More specifically we aim to: 1) Collect multisession and multimodal data from patients at a risk of LBDs, and compare them to patients with probable or clinically established PD and probable DLB, Alzheimer’s disease and age- and gender-matched healthy controls. 2) Identify prodromal markers of LBDs based on longitudinal analysis of complex clinical, paraclinical, neuropsychological, neurophysiological and multimodal imaging data 3) Describe complex pathophysiological mechanisms of LBDs and subtle symptoms that are difficult to be perceived. 4) To integrate the gained knowledge into a new open-source LBDs decision support system based on the stateof- the-art machine learning algorithms.

*It is supposed that the final version of the software will be released in 2023, nevertheless, some key parts (e.g. extraction of features) can be already used.*

*Development of this software is supported by Ministry of Health of the Czech Republic, grant nr. NU20-04-00294 (https://starfos.tacr.cz/en/project/NU20-04-00294). All rights reserved.*
