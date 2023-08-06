#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##################################################################################################
# Copyright (c) 2022-2023, Laboratorio de Microprocesadores
# Facultad de Ciencias Exactas y Tecnología, Universidad Nacional de Tucumán
# https://www.microprocesadores.unt.edu.ar/
#
# Copyright (c) 2022-2023, Esteban Volentini <evolentini@herrera.unt.edu.ar>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
# OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023, Esteban Volentini <evolentini@herrera.unt.edu.ar>
##################################################################################################

from siru.preat import Preat, Result
from siru.gpio import Output, Input

port = "/dev/tty.usbserial-141201"
preat = Preat(port)

key_left = Output(preat, 0)
key_up = Output(preat, 1)
key_right = Output(preat, 2)
key_down = Output(preat, 3)
key_accept = Output(preat, 4)
key_cancel = Output(preat, 5)

led_red = Input(preat, 0)
led_yellow = Input(preat, 1)
led_green = Input(preat, 2)
rgb_red = Input(preat, 4)
rgb_green = Input(preat, 5)
rgb_blue = Input(preat, 3)

assert key_left.clear() == Result.NO_ERROR
assert preat.wait(0, 200, [led_red.has_falling], key_left.set) == Result.NO_ERROR
assert preat.wait(0, 200, [led_red.has_rising], key_left.clear) == Result.NO_ERROR

assert key_up.clear() == Result.NO_ERROR
assert preat.wait(0, 200, [led_yellow.has_falling], key_up.set) == Result.NO_ERROR
assert preat.wait(0, 200, [led_yellow.has_rising], key_up.clear) == Result.NO_ERROR

assert key_right.clear() == Result.NO_ERROR
assert preat.wait(0, 200, [led_green.has_falling], key_right.set) == Result.NO_ERROR
assert preat.wait(0, 200, [led_green.has_rising], key_right.clear) == Result.NO_ERROR

assert key_cancel.clear() == Result.NO_ERROR
assert preat.wait(0, 200, [rgb_red.has_falling], key_cancel.set) == Result.NO_ERROR
assert preat.wait(0, 200, [rgb_red.has_rising], key_cancel.clear) == Result.NO_ERROR

assert key_down.clear() == Result.NO_ERROR
assert preat.wait(0, 200, [rgb_green.has_falling], key_down.set) == Result.NO_ERROR
assert preat.wait(0, 200, [rgb_green.has_rising], key_down.clear) == Result.NO_ERROR

assert key_accept.clear() == Result.NO_ERROR
assert preat.wait(0, 1200, [rgb_blue.has_falling], key_accept.set) == Result.NO_ERROR
assert preat.wait(0, 1200, [rgb_blue.has_rising], key_accept.clear) == Result.NO_ERROR
