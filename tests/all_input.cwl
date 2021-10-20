#!/usr/bin/env cwl-runner
cwlVersion: v1.2
class: Workflow
inputs:
  - id: file
    type: File
    label: "File label"
    doc: "File doc"
  - id: file_default
    type: File
    default:
      class: File
      path: test.txt
    label: "File default label"
    doc: "File default doc"
  - id: file_array
    type: File[]
    label: "File array label"
    doc: "File array doc"
  - id: file_not_require
    type: File?
    label: "File not require label"
    doc: "File not require doc"
  - id: file_with_secondaryFiles
    type: File
    secondaryFiles:
      - ".foo"
      - ".bar"
    label: "File with secondaryFiles label"
    doc: "File with secondaryFiles doc"
  - id: directory
    type: Directory
    label: "Directory label"
    doc: "Directory doc"
  - id: directory_array
    type: Directory[]
    label: "Directory array label"
    doc: "Directory array doc"
  - id: directory_not_require
    type: Directory?
    label: "Directory not require label"
    doc: "Directory not require doc"
  - id: string
    type: string
    label: "string label"
    doc: "string doc"
  - id: string_default
    type: string
    default: "default_value"
    label: "string default label"
    doc: "string default doc"
  - id: string_array
    type:
      type: array
      items: string
    label: "string array label"
    doc: "string array doc"
  - id: string_array_2
    type: string[]
    label: "string array_2 label"
    doc: "string array_2 doc"
  - id: string_not_require
    type: string?
    label: "string not require label"
    doc: "string not require doc"
  - id: int
    type: int
    label: "int label"
    doc: "int doc"
  - id: int_default
    type: int
    default: 1
    label: "int default label"
    doc: "int default doc"
  - id: int_array
    type:
      type: array
      items: int
    label: "int array label"
    doc: "int array doc"
  - id: int_array_2
    type: int[]
    label: "int array 2 label"
    doc: "int array 2 doc"
  - id: int_not_require
    type: int?
    label: "int not require label"
    doc: "int not require doc"
  - id: any
    type: Any
    label: "Any label"
    doc: "Any doc"
  - id: any_default
    type: Any
    default: "default_value"
    label: "any default label"
    doc: "any default doc"
  - id: any_array
    type:
      type: array
      items: Any
    label: "any array label"
    doc: "any array doc"
  - id: any_array_2
    type: Any[]
    label: "any array 2 label"
    doc: "any array 2 doc"
  - id: boolean
    type: boolean
    label: "boolean label"
    doc: "boolean doc"
  - id: boolean_default
    type: boolean
    default: true
    label: "boolean default label"
    doc: "boolean default doc"
  - id: boolean_not_require
    type: boolean?
    label: "boolean not require label"
    doc: "boolean not require doc"
steps: []
outputs: []
