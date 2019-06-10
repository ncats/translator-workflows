#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: python biocwl.py run
inputs:
  message:
    type: string
    inputBinding:
      position: 1
outputs: []
