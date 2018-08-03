#!/usr/bin/env python3

# pylint: disable=missing-docstring
import unittest

import temppathlib

import posixfs


class TestDirectorySync(unittest.TestCase):
    def test_that_it_doesnt_panic(self):  # pylint: disable=no-self-use
        with temppathlib.TemporaryDirectory() as tmp_dir:
            pth = tmp_dir.path / 'file.txt'
            with open(str(pth), 'wt') as fid:
                fid.write('oi')
                fid.flush()

            posixfs.fsync_directory(path=tmp_dir.path)


class TestAtomicWritingBytes(unittest.TestCase):
    def test_with_empty(self):
        with temppathlib.TemporaryDirectory() as tmp_dir:
            pth = tmp_dir.path / 'file.txt'

            with posixfs.AtomicWritingBytes(path=pth) as fid:
                fid.write(b'')

            data = pth.read_bytes()
            self.assertEqual(data, b'')

    def test_with_data(self):
        with temppathlib.TemporaryDirectory() as tmp_dir:
            pth = tmp_dir.path / 'file.txt'

            with posixfs.AtomicWritingBytes(path=pth) as fid:
                fid.write(b'hello')

            data = pth.read_bytes()
            self.assertEqual(data, b'hello')

    def test_durable_doesnt_panic(self):
        with temppathlib.TemporaryDirectory() as tmp_dir:
            pth = tmp_dir.path / 'file.txt'

            with posixfs.AtomicWritingBytes(path=pth, durable=True) as fid:
                fid.write(b'hello')

            data = pth.read_bytes()
            self.assertEqual(data, b'hello')


class TestAtomicWriteBytes(unittest.TestCase):
    def test_that_it_works(self):
        with temppathlib.TemporaryDirectory() as tmp_dir:
            pth = tmp_dir.path / 'file.txt'
            posixfs.atomic_write_bytes(path=pth, data=b'hello', durable=True)

            data = pth.read_bytes()
            self.assertEqual(data, b'hello')


class TestAtomicWritingText(unittest.TestCase):
    def test_with_empty(self):
        with temppathlib.TemporaryDirectory() as tmp_dir:
            pth = tmp_dir.path / 'file.txt'

            with posixfs.AtomicWritingText(path=pth) as fid:
                fid.write('')

            text = pth.read_text()
            self.assertEqual(text, '')

    def test_with_text(self):
        with temppathlib.TemporaryDirectory() as tmp_dir:
            pth = tmp_dir.path / 'file.txt'

            with posixfs.AtomicWritingText(path=pth) as fid:
                fid.write('hello')

            text = pth.read_text()
            self.assertEqual(text, 'hello')

    def test_durable_doesnt_panic(self):
        with temppathlib.TemporaryDirectory() as tmp_dir:
            pth = tmp_dir.path / 'file.txt'

            with posixfs.AtomicWritingText(path=pth, durable=True) as fid:
                fid.write('hello')

            text = pth.read_text()
            self.assertEqual(text, 'hello')


class TestAtomicWriteText(unittest.TestCase):
    def test_that_it_works(self):
        with temppathlib.TemporaryDirectory() as tmp_dir:
            pth = tmp_dir.path / 'file.txt'
            posixfs.atomic_write_text(path=pth, text='hello', durable=True)

            text = pth.read_text()
            self.assertEqual(text, 'hello')


if __name__ == '__main__':
    unittest.main()
