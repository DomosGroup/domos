#    Copyright (C) 2016  Domos Group
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import peripherals.peripheral as peripheral
import peripherals.commands as commands


class TEMP001(peripheral.Peripheral):
    supported_firmwares = [100]
    commands = [
        commands.UnrecognizedCommand(),
        commands.Info(),
        commands.Temperature(),
    ]
