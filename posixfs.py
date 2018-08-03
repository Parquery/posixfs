""" provides atomic and durable writes on a posix file system. """
import io
import os
import pathlib
import tempfile
from typing import Union, Optional, Any, BinaryIO, TextIO, cast  # pylint: disable=unused-import


def fsync_directory(path: Union[str, pathlib.Path]) -> None:
    """
    fsyncs a directory so that any renames are made durable.

    :param path: to the directory
    :return:
    """
    fid = os.open(str(path), os.O_RDONLY)
    try:
        os.fsync(fid)
    finally:
        if fid >= 0:
            os.close(fid)


def atomic_write_bytes(path: Union[str, pathlib.Path], data: bytes, durable: bool = False) -> None:
    """
    writes the data to the file atomically.

    :param path: to the file
    :param data: content to write
    :param durable: if set, makes the write durable as well
    :return:
    """
    with AtomicWritingBytes(path=path, durable=durable) as fid:
        fid.write(data)


def atomic_write_text(path: Union[str, pathlib.Path], text: str, encoding='utf-8', durable: bool = False) -> None:
    """
    writes the text to the file atomically.

    :param path: to the file
    :param text: content to write
    :param encoding: of the text
    :param durable: if set, makes the write durable as well
    :return:
    """
    with AtomicWritingText(path=path, encoding=encoding, durable=durable) as fid:
        fid.write(text)


class AtomicWritingBytes:
    """
    manages the context of an atomic write of bytes.
    """

    def __init__(self, path: Union[str, pathlib.Path], durable: bool = False) -> None:
        """
        :param path: to the file
        :param durable: if set, makes the write durable as well.
        """
        if isinstance(path, str):
            self.path = pathlib.Path(path)
        elif isinstance(path, pathlib.Path):
            self.path = path
        else:
            raise ValueError("Unexpected type of 'path': {}".format(type(path)))

        self.durable = durable

        # mypy does not support tempfile.NamedTemporaryFile; see https://github.com/python/mypy/issues/3094
        self._tmp = None  # type: Optional[Any]

    def close(self) -> None:
        """
        closes the atomic writing. If already closed, this function has no effect.
        """
        if self._tmp is not None:
            renamed = False
            try:
                self._tmp.file.flush()
                os.rename(self._tmp.name, self.path.as_posix())
                renamed = True

                if self.durable:
                    fsync_directory(path=self.path.parent)

            finally:
                self._tmp.close()
                if not renamed:
                    os.unlink(self._tmp.name)

            self._tmp = None

    def __enter__(self) -> BinaryIO:
        self._tmp = tempfile.NamedTemporaryFile(dir=self.path.parent.as_posix(), prefix=self.path.name, delete=False)
        fid = self._tmp.file  # type: ignore
        return cast(BinaryIO, fid)

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()


class AtomicWritingText:
    """
    manages the context of an atomic write of text.
    """

    def __init__(self, path: Union[str, pathlib.Path], encoding: str = 'utf-8', durable: bool = False) -> None:
        """
        :param path: to the file
        :param encoding: of the text
        :param durable: if set, makes the write durable as well.
        """
        if isinstance(path, str):
            self.path = pathlib.Path(path)
        elif isinstance(path, pathlib.Path):
            self.path = path
        else:
            raise ValueError("Unexpected type of 'path': {}".format(path))

        self.encoding = encoding
        self.durable = durable

        self._wrapper = None  # type: Optional[io.TextIOWrapper]
        self._writing_bytes = None  # type: Optional[AtomicWritingBytes]

    def close(self) -> None:
        """ closes the atomic writing. If already closed, this function has no effect. """
        if self._writing_bytes is not None:
            assert self._wrapper is not None, "Unexpected self._wrapper None when self._writing_bytes is not None."
            self._wrapper.flush()
            self._wrapper.detach()
            self._wrapper = None

            self._writing_bytes.close()
            self._writing_bytes = None

    def __enter__(self) -> TextIO:
        self._writing_bytes = AtomicWritingBytes(path=self.path, durable=self.durable)

        fid = self._writing_bytes.__enter__()
        self._wrapper = io.TextIOWrapper(fid, encoding=self.encoding)

        return cast(TextIO, self._wrapper)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
