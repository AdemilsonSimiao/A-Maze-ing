from __future__ import annotations

import ctypes
import os
from typing import Callable, cast

KeyCallback = Callable[[int], int]
LoopCallback = Callable[[], int]


class MLXError(RuntimeError):
	...

class MLX:

    def __init__(self, lib_path: str = "./libmlx_shim.so") -> None:
        if not os.path.exists(lib_path):
            raise MLXError(f"{lib_path} not found -- run `make mlx-shim` first.")
        self._lib = ctypes.CDLL(lib_path)
        self._bind_signatures()

        self._callbacks: list[object] = []
        self.mlx_ptr = self._lib.mlx_init()
        if not self.mlx_ptr:
            raise MLXError("mlx_init() failed -- is a display available?")

    def _bind_signatures(self) -> None:

        lib = self._lib
        lib.mlx_init.restype = ctypes.c_void_p
        lib.mlx_new_window.restype = ctypes.c_void_p
        lib.mlx_new_window.argtypes = [
            ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p,
        ]
        lib.mlx_pixel_put.argtypes = [
            ctypes.c_void_p, ctypes.c_void_p,
            ctypes.c_int, ctypes.c_int, ctypes.c_int,
        ]
        lib.mlx_loop.argtypes = [ctypes.c_void_p]
        lib.mlx_destroy_window.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

    def new_window(self, width: int, height: int, title: str) -> int:
        win = self._lib.mlx_new_window(self.mlx_ptr, width, height, title.encode())
        if not win:
            raise MLXError("mlx_new_window() failed.")
        return cast(int, win)

    def pixel_put(self, win: int, x: int, y: int, color: int) -> None:
        self._lib.mlx_pixel_put(self.mlx_ptr, win, x, y, color)

    def on_key(self, win: int, callback: KeyCallback) -> None:
        c_callback = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_void_p)(
            lambda keycode, _param: callback(keycode)
        )
        self._callbacks.append(c_callback)
        self._lib.mlx_key_hook(win, c_callback, None)

    def on_loop(self, callback: LoopCallback) -> None:
        c_callback = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p)(
            lambda _param: callback()
        )
        self._callbacks.append(c_callback)
        self._lib.mlx_loop_hook(self.mlx_ptr, c_callback, None)

    def loop(self) -> None:
        self._lib.mlx_loop(self.mlx_ptr)

    def destroy_window(self, win: int) -> None:
        self._lib.mlx_destroy_window(self.mlx_ptr, win)