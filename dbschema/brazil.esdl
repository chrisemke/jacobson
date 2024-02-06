# Jacobson is a self hosted zipcode API
# Copyright (C) 2023-2024  Christian G. Semke.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

module brazil {
    type Address {
        required zipcode: int32 {
            constraint exclusive;
            constraint max_len_value(8);
        }
        required coords: tuple<lat: float64, long: float64, altitude: float64>;
        district: str;
        complement: str;
        neighborhood: str;
        multi link city: City;
        multi link state: State;

    }
    type City {
        required ibge: int32;
        required name: str;
    }

    scalar type Acronyms extending enum<AC, AL, AP, AM, BA, CE, DF, ES, GO, MA, MT, MS, MG, PA, PB, PR, PE, PI, RJ, RN, RS, RO, RR, SC, SP, SE, TO>;

    type State {
        required name: str {
            constraint exclusive;
        }
        required acronym: Acronyms {
            constraint exclusive;
        }
    }
}
