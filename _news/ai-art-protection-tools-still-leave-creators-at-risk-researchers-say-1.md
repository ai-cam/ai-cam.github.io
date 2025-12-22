---
title: AI art protection tools still leave creators at risk, researchers say
excerpt: "Artists urgently need stronger defences to protect their work from
  being used to train AI models without their consent.  "
cover_image: /assets/images/uploads/about-find-3.png
date: 2025-06-23
tags:
  - tag: Research and Innovation
information: /
apply_link: /
apply_link_text: /
---
Artists urgently need stronger defences to protect their work from being used to train AI models without their consent.  

So say a team of researchers who have uncovered significant weaknesses in two of the art protection tools most used by artists to safeguard their work.

According to their creators, Glaze and NightShade were both developed to protect human creatives against the invasive uses of generative artificial intelligence.

The tools are popular with digital artists who want to stop artificial intelligence models (like the AI art generator Stable Diffusion) from copying their unique styles without consent. Together, Glaze and NightShade have been downloaded almost nine million times.

But according to an international group of researchers, these tools have critical weaknesses that mean they cannot reliably stop AI models from training on artists’ work.

The tools add subtle, invisible distortions (known as poisoning perturbations) to digital images. These ‘poisons’ are designed to confuse AI models during training. Glaze takes a passive approach, hindering the AI model’s ability to extract key stylistic features. NightShade goes further, actively corrupting the learning process by causing the AI model to associate an artist’s style with unrelated concepts.

But the researchers have created a method – called LightShed – that can bypass these protections. LightShed can detect, reverse-engineer and remove these distortions, effectively stripping away the poisons and rendering the images usable again for Generative AI model training.

It was developed by researchers at the University of Cambridge along with colleagues at the Technical University Darmstadt and the University of Texas at San Antonio. The researchers hope that by publicising their work – which will be presented at the USENIX Security Symposium, a major security conference, in August – they can let creatives know that there are major issues with art protection tools.

LightShed works through a three-step process. It first identifies whether an image has been altered with known poisoning techniques.

In a second, reverse engineering step, it learns the characteristics of the perturbations using publicly available poisoned examples. Finally, it eliminates the poison to restore the image to its original, unprotected form.

Continue to read the full article here
