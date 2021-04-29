#!/usr/bin/python3
#/*
# * Copyright (c) 2021 Florian Becker <fb@vxapps.com> (VX APPS).
# * All rights reserved.
# *
# * Redistribution and use in source and binary forms, with or without
# * modification, are permitted provided that the following conditions are met:
# *
# * 1. Redistributions of source code must retain the above copyright notice, this
# *    list of conditions and the following disclaimer.
# *
# * 2. Redistributions in binary form must reproduce the above copyright notice,
# *    this list of conditions and the following disclaimer in the documentation
# *    and/or other materials provided with the distribution.
# *
# * 3. Neither the name of the copyright holder nor the names of its
# *    contributors may be used to endorse or promote products derived from
# *    this software without specific prior written permission.
# *
# * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# */

import sys
import xml.etree.ElementTree as ET

file = sys.argv[1]

tree = ET.parse(file)
root = tree.getroot()

qbuttongroups = []
qbuttongroups_exclusive = []

# Find all: <widget class="Q3ButtonGroup"
for buttonGroup in root.findall(".//widget[@class='Q3ButtonGroup']"):
  name = buttonGroup.get('name')
  print(name)
  qbuttongroups.append(name)

  # Change Q3ButtonGroup to QGroupBox
  buttonGroup.set('class', 'QGroupBox')
  buttonGroup.set('name', 'gb'+name)
  
  # Find exclusive and save state
  exclusive = buttonGroup.find("property[@name='exclusive']/bool")
  if exclusive is not None:
    qbuttongroups_exclusive.append(exclusive.text)
  else:
    qbuttongroups_exclusive.append('true')

  # Add buttonGroup property to all QCheckBox, QPushButton, QRadioButton, and QToolButton
  for button in buttonGroup.findall(".//widget"):
    className = button.get('class')
    # Add buttonGroup property
    # <attribute name="buttonGroup">
    #   <string notr="true">buttonGroupName</string>
    # </attribute>
    if className == 'QCheckBox' or className == 'QPushButton' or className == 'QRadioButton' or className == 'QToolButton':
      attribute = ET.Element('attribute')
      attribute.set('name', 'buttonGroup')

      subtype = ET.Element('string')
      subtype.set('notr','true')
      subtype.text = name
      attribute.append(subtype)

      button.append(attribute)

# Add buttongroups to root
# <buttongroups>
#  <buttongroup name="buttonGroup"/>
# </buttongroups>
groups = ET.Element('buttongroups')
for qbuttongroup in qbuttongroups:
  index = qbuttongroups.index(qbuttongroup)
  exclusive = qbuttongroups_exclusive[index]

  group = ET.Element('buttongroup')
  group.set('name',qbuttongroup)
  # true is default
  if exclusive == 'false':
    exclusiveElement = ET.Element('property')
    exclusiveElement.set('name', 'exclusive')
    
    subtype = ET.Element('bool')
    subtype.text = exclusive
    exclusiveElement.append(subtype)
    
    group.append(exclusiveElement)
  groups.append(group)
root.append(groups)

tree.write(file, encoding="UTF-8", xml_declaration=True)
