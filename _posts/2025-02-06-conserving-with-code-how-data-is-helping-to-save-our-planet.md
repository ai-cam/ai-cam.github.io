---
layout: blog-single
permalink: /blog/:title
title: "Conserving with code: How data is helping to save our planet "
excerpt: Over the last two decades, the University of Cambridge-based project
  Conservation Evidence has screened more than 1.5 million scientific papers on
  conservation, as well as manually summarising 8,600+ studies relating to
  conservation actions.18 It has taken an estimated 75-person years for a team
  of highly skilled and highly trained researchers to manually curate the
  current database, which is used by a wide range of organisations to help
  inform decisions that are increasingly vital to the future of our planet and
  biodiversity conservation. Using the current manual system, only a few hundred
  new papers can be added to the open access database each year. AI has opened
  up new possibilities.
date: 2025-02-05T00:00:00+00:00
category:
  - policy
image: /assets/uploads/getty-images-4r9ysoxez2a-unsplash-1-.jpg
---
Over the last two decades, the University of Cambridge-based project Conservation Evidence has screened more than 1.5 million scientific papers on conservation, as well as manually summarising 8,600+ studies relating to conservation actions.18 It has taken an estimated 75-person years for a team of highly skilled and highly trained researchers to manually curate the current database, which is used by a wide range of organisations to help inform decisions that are increasingly vital to the future of our planet and biodiversity conservation. Using the current manual system, only a few hundred new papers can be added to the open access database each year. AI has opened up new possibilities.

Planetary Computing Fellow Dr Sadiq Jafferand zoologist Dr Alec Christie, Henslow Research Fellow at Downing College, are part of an interdisciplinary team of scientists from the University of Cambridge who are using AI to accelerate the synthesis. Building on the work of the Conservation Evidence team, the aim is to create a transformative tool for conservation research. “What we decided to do was to look at this as a way of building systems around the existing team to make them a lot more productive,” explains Dr Jaffer. “So there’s always a human in the middle of things who is accountable for the decisions that are made. But there are AI systems that can increase their productivity significantly.”

To start with, Dr Jaffer and his colleagues compared Conservation Evidence’s curated collection of papers with a broader sample of scientific literature. Using advanced language models, they clustered these papers by topic such as amphibians, reptiles, birds, and other species, confirming there was a clear structure in the data that could be leveraged for further analysis. Funded through a range of sources including ai@cam, The Hans Wilsdorf Foundation, and other philanthropic donations, this work allowed the team to break down research into smaller, more meaningful categories. With this groundwork in place, they developed an innovative three-step AI pipeline designed to streamline the identification of relevant conservation research.

In the first step of the project, smaller language models sifted through the OpenAlex dataset – an open data research platform that publishes metadata on around 250 million academic papers – to identify potentially useful papers. This analysis narrowed the sample of literature for analysis down to 6 million papers. From there, the team built a system that can download the abstracts and PDFs for each of the papers from relevant publishers and rank them according to their relevance. 

After that, a set of 100,000 papers was filtered using a Large Language Model – similar to those powering ChatGPT – which applied the same criteria a human reviewer would use to assess each paper’s relevance. This system is now being tested against human judgements, and early results indicate strong alignment between AI and human evaluations, showing promise for its future use in automating the review process, according to Dr Jaffer.

This is one of the first times data mining has been applied on such a large scale for conservation literature, as far as Dr Jaffer is aware, paving the way for more industrial-scale approach to gathering evidence. What makes the project particularly innovative is the fact that they are building a living system that can be expanded week on week with new papers. As researchers select more papers, the AI-driven system becomes more precise and finds more relevant evidence. 

The team is now focusing on steps two and three of the process: extracting deeper insights from the full-text PDFs of relevant papers and integrating this information into Conservation Evidence’s existing database. But the project has not been without its challenges.

#### Legal and technical headaches

“The biggest barrier was actually getting data from the publishers,” says Dr Jaffer. “The OpenAlex data set is freely available, but it provides just the titles and metadata for papers and not the abstracts. Some publishers are quite free with their abstracts because they realise that having them out there in the wild means that there’s more chance of people discovering their papers. Unfortunately, some of the biggest publishers are not.”

In theory, copyright issues should not have been a problem because text and data mining for academic research (or noncommercial uses) is exempt from copyright rules set by the Copyright, Designs and Patents Act 1988. However, the team had a range of responses from publishers when they got in touch about downloading the data they needed, even though the data was technically Open Access and available under a Creative Commons License. 

Some publishers were happy to give the go ahead and evenpointed the team to the code for bulk downloading their papers on the coding platform GitHub. One example of best practice in this regard was the nonprofit, Open Access publisher PLOS. Other publishers insisted the team had to go through complicated Application Programme Interfaces (APIs), which threw up a range of technical and legal issues. Dr Jaffer and his colleagues had to write custom code to access each publisher’s data. It took around three to four months of negotiating to reach agreement with some of the bigger publishers, with support from the University Library and JISC – the UK digital, data, and technology agency focused on tertiary education, research, and innovation. 

“We’ve got AI models that can really accelerate these kinds of syntheses to provide evidence for policy-makers but if the publishers are going to be gatekeepers, it’s going to slow down our progress in doing that,” Dr Jaffer says. “And the sad thing is that the government has paid money via research grants to pay for this Open Access material to be made available and yet we can’t actually go and download it.”