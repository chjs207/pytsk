#!/usr/bin/python
#
# Copyright 2013, Joachim Metz <joachim.metz@gmail.com>.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import pytsk3
import unittest

import test_lib


# mmls ../test_data/tsk_volume_system.raw 
# DOS Partition Table
# Offset Sector: 0
# Units are in 512-byte sectors
# 
#      Slot    Start        End          Length       Description
# 00:  Meta    0000000000   0000000000   0000000001   Primary Table (#0)
# 01:  -----   0000000000   0000000000   0000000001   Unallocated
# 02:  00:00   0000000001   0000000350   0000000350   Linux (0x83)
# 03:  Meta    0000000351   0000002879   0000002529   DOS Extended (0x05)
# 04:  Meta    0000000351   0000000351   0000000001   Extended Table (#1)
# 05:  -----   0000000351   0000000351   0000000001   Unallocated
# 06:  01:00   0000000352   0000002879   0000002528   Linux (0x83)


class TSKVolumeInfoTestCase(unittest.TestCase):
  """The test case for the Volume_Info object."""
  maxDiff = None

  def _testInitialize(self, volume_info):
    """Test the initialize functionality.

    Args:
      volume_info: the Volume_Info object.
    """
    self.assertNotEquals(volume_info, None)

  def _testIterate(self, volume_info):
    """Test the iterate functionality.

    Args:
      volume_info: the Volume_Info object.
    """
    parts = []

    for part in volume_info:
      part_string = (
          u'{0:02d}:  {1:010d}   {2:010d}   {3:010d}   {4:s}\n').format(
              part.addr, part.start, part.start + part.len - 1, part.len,
              part.desc.decode('utf-8'))
      parts.append(part_string)

    self.assertEquals(len(parts), 7)

    expected_parts_string = (
        u'00:  0000000000   0000000000   0000000001   Primary Table (#0)\n'
        u'01:  0000000000   0000000000   0000000001   Unallocated\n'
        u'02:  0000000001   0000000350   0000000350   Linux (0x83)\n'
        u'03:  0000000351   0000002879   0000002529   DOS Extended (0x05)\n'
        u'04:  0000000351   0000000351   0000000001   Extended Table (#1)\n'
        u'05:  0000000351   0000000351   0000000001   Unallocated\n'
        u'06:  0000000352   0000002879   0000002528   Linux (0x83)\n')

    self.assertEquals(u''.join(parts), expected_parts_string)


class TSKVolumeInfoTest(TSKVolumeInfoTestCase):
  """The unit test for the Volume_Info object."""

  def setUp(self):
    """Sets up the needed objects used throughout the test."""
    test_file = os.path.join('test_data', 'tsk_volume_system.raw')
    self._img_info = pytsk3.Img_Info(test_file)

  def testInitialize(self):
    """Test the initialize functionality."""
    volume_info = pytsk3.Volume_Info(self._img_info)
    self._testInitialize(volume_info)

  def testIterate(self):
    """Test the iterate functionality."""
    volume_info = pytsk3.Volume_Info(self._img_info)
    self._testIterate(volume_info)


class TSKVolumeInfoBogusTest(TSKVolumeInfoTestCase):
  """The unit test for the Volume_Info object that should fail."""

  def setUp(self):
    """Sets up the needed objects used throughout the test."""
    test_file = os.path.join('test_data', 'bogus.raw')
    self._img_info = pytsk3.Img_Info(test_file)

  def testInitialize(self):
    """Test the initialize functionality."""
    with self.assertRaises(IOError):
      volume_info = pytsk3.Volume_Info(self._img_info)


class TSKVolumeInfoFileObjectTest(TSKVolumeInfoTestCase):
  """The unit test for the Volume_Info object using an Img_Info file-like object."""

  def setUp(self):
    """Sets up the needed objects used throughout the test."""
    test_file = os.path.join('test_data', 'tsk_volume_system.raw')
    self._file_object = open(test_file, 'rb')

    stat_info = os.stat(test_file)
    self._file_size = stat_info.st_size
    self._img_info = test_lib.FileObjectImageInfo(
        self._file_object, self._file_size)

  def testInitialize(self):
    """Test the initialize functionality."""
    volume_info = pytsk3.Volume_Info(self._img_info)
    self._testInitialize(volume_info)

  def testIterate(self):
    """Test the iterate functionality."""
    volume_info = pytsk3.Volume_Info(self._img_info)
    self._testIterate(volume_info)


class TSKVolumeInfoFileObjectWithDetectTest(TSKVolumeInfoTestCase):
  """The unit test for the Volume_Info object using an Img_Info file-like object.
     with image type: pytsk3.TSK_IMG_TYPE_DETECT."""

  def setUp(self):
    """Sets up the needed objects used throughout the test."""
    test_file = os.path.join('test_data', 'tsk_volume_system.raw')
    self._file_object = open(test_file, 'rb')

    stat_info = os.stat(test_file)
    self._file_size = stat_info.st_size
    self._img_info = test_lib.FileObjectImageInfo(
        self._file_object, self._file_size,
        image_type=pytsk3.TSK_IMG_TYPE_DETECT)

  def testInitialize(self):
    """Test the initialize functionality."""
    volume_info = pytsk3.Volume_Info(self._img_info)
    self._testInitialize(volume_info)

  def testIterate(self):
    """Test the iterate functionality."""
    volume_info = pytsk3.Volume_Info(self._img_info)
    self._testIterate(volume_info)


class TSKVolumeInfoFileObjectTest(TSKVolumeInfoTestCase):
  """The unit test for the Volume_Info object using an Img_Info file-like object
     with a large size."""

  def setUp(self):
    """Sets up the needed objects used throughout the test."""
    test_file = os.path.join('test_data', 'tsk_volume_system.raw')
    self._file_object = open(test_file, 'rb')

    self._file_size = 1024 * 1024 * 1024 * 1024
    self._img_info = test_lib.FileObjectImageInfo(
        self._file_object, self._file_size)

  def testInitialize(self):
    """Test the initialize functionality."""
    volume_info = pytsk3.Volume_Info(self._img_info)
    self._testInitialize(volume_info)

  def testIterate(self):
    """Test the iterate functionality."""
    volume_info = pytsk3.Volume_Info(self._img_info)

    parts = []

    for part in volume_info:
      part_string = (
          u'{0:02d}:  {1:010d}   {2:010d}   {3:010d}   {4:s}\n').format(
              part.addr, part.start, part.start + part.len - 1, part.len,
              part.desc.decode('utf-8'))
      parts.append(part_string)

    # Note that due to the size the SleuthKit will add a non-existing part:
    # 07:  0000002880   2147483647   2147480768   Unallocated

    self.assertEquals(len(parts), 8)

    expected_parts_string = (
        u'00:  0000000000   0000000000   0000000001   Primary Table (#0)\n'
        u'01:  0000000000   0000000000   0000000001   Unallocated\n'
        u'02:  0000000001   0000000350   0000000350   Linux (0x83)\n'
        u'03:  0000000351   0000002879   0000002529   DOS Extended (0x05)\n'
        u'04:  0000000351   0000000351   0000000001   Extended Table (#1)\n'
        u'05:  0000000351   0000000351   0000000001   Unallocated\n'
        u'06:  0000000352   0000002879   0000002528   Linux (0x83)\n'
        u'07:  0000002880   2147483647   2147480768   Unallocated\n')

    self.assertEquals(u''.join(parts), expected_parts_string)


if __name__ == '__main__':
  unittest.main()
