---
layout: report-single
title: "A future vision for AI: public perspectives on the role of AI and the Missions for Government"
type: policy
date: 2024-03-01
authors:
  - given: "Jessica"
    preferred: "Jess"
    family: "Montgomery"
    affiliation: "ai@cam, University of Cambridge"
  - given: "Neil D."
    preferred: "Neil"
    family: "Lawrence"
    affiliation: "ai@cam, University of Cambridge"
institution: "ai@cam"
abstract: "This report presents findings from public dialogue workshops conducted in Liverpool and Cambridge to understand public perspectives on the role of AI in delivering the Missions for Government. The dialogue focused on four key areas: crime and policing, education, energy and net zero, and health. Through conversations with 40 members of the public and AI experts from multiple universities, the report outlines key recommendations for shaping AI development in public services to ensure widespread public benefit."
people:
  - "Jess Montgomery"
  - "Neil Lawrence"
  - "Mo Vali"
download_url: "/assets/uploads/ai-cam-public-dialogue-report.pdf"
key_findings:
  - "Need for transparency around AI use in public services"
  - "Governance frameworks prioritizing public benefit over profit"
  - "Independent regulatory oversight with enforcement powers"
  - "User-centered design practices to remove bias and improve reliability"
  - "Data sharing regulations balancing privacy and public benefit"
  - "Robust security systems against AI-related cyber threats"
recommendations:
  - "AI should not replace human contact in public services"
  - "AI should support rather than replace human decision-making"
  - "Service users and staff must be involved in AI implementation decisions"
  - "Administrative AI tools can free up frontline staff time for patient care"
excerpt: "Last month ai@cam convened public dialogue workshops in Liverpool and Cambridge to better understand public perspectives on the role of AI in delivering the Missions for Government, focusing on crime and policing, education, energy and net zero, and health."
category:
  - policy
  - dialogue
image: /assets/uploads/ai-for-public-dialgoue.jpeg
pdf: /assets/uploads/ai-cam-public-dialogue-report.pdf
date: 2024-10-28
---

This report presents findings from public dialogue workshops exploring perspectives on AI in public services. Through structured conversations between members of the public and AI experts, the dialogue examined opportunities and challenges for AI deployment across key public service areas.

## Key Findings

The dialogue revealed clear public priorities for AI governance and implementation:

{% for finding in page.key_findings %}
- {{ finding }}
{% endfor %}

## Recommendations

The workshops generated several key recommendations for AI deployment in public services:

{% for rec in page.recommendations %}
- {{ rec }}
{% endfor %}

## Expert Perspectives

{% assign mo = site.people | where: "name", "Mo Vali" | first %}
{{ mo.given }} {{ mo.family }} emphasized: "The discussions today highlighted clearly that participants did not want to lose that human-to-human interaction when engaging with public services. It is crucial we do not underestimate the value we place on personalised, sensitive and individual human interaction, especially when it comes to our teachers, nurses, and doctors."

{% assign jess = site.people | where: "name", "Jess Montgomery" | first %}
{{ jess.given }} {{ jess.family }}, Director of ai@cam, noted: "We need new ways of centring social interests and needs in policy and technology development around AI. Engaging the public in a conversation about our shared vision for AI technologies plays an important role in connecting advances in technology and policy to public benefit."

{% assign neil = site.people | where: "name", "Neil Lawrence" | first %}
{{ neil.given }} {{ neil.family }}, Chair for ai@cam, concluded: "The challenge for the next wave of AI development is to create meaningful, real-world benefits for individuals, communities, and society. Giving people the confidence that the voice is not only important but *heard* allows us to build the bridges between organisations and communities that can drive real progress in AI research."

## Download the Full Report

The complete findings and recommendations can be found in the [full report]({{ page.download_url }}). 