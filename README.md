# BDAL Powerlifting Viva Guide

A single-page study guide for the Big Data Analytics Lab (CSE 4346) final project:
the OpenPowerlifting dataset analysed with Hadoop 3.4.1 MapReduce and Apache Pig 0.17.0.

**Live site:** https://shinzuu.github.io/bdal-powerlifting-viva/

What's inside:

- The dataset: source, licence, size, all 42 columns, the 7 columns the jobs use, Total vs Dots
- How the project was built, step by step, and the problems hit along the way
- Theory: HDFS, YARN, the MapReduce data flow, Pig Latin
- Every line of the 3 MapReduce jobs and 5 Pig scripts, with numbered explanations
- Lab 2 (basic HDFS commands) with real terminal output and error messages
- Terminal command reference and a type-it-yourself drill
- About 80 viva questions, a multiple-choice quiz and fill-in-the-blanks

The project code is at https://github.com/Shinzuu/openpowerlifting-hadoop-analysis.
`build.py` regenerates `index.html` from a local checkout of the project, so the code
listings always match the files that ran.

Data: OpenPowerlifting, https://www.openpowerlifting.org (public domain).
