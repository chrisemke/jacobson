# Jacobson is a self hosted zipcode API
# Copyright (C) 2023  Christian G. Semke
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

CREATE MIGRATION m1t5im7wi6t5m6pnffk3glbeow6g425rrs6oamplfrrzsa3tnr42ba
    ONTO initial
{
  CREATE MODULE brazil IF NOT EXISTS;
  CREATE FUTURE nonrecursive_access_policies;
  CREATE TYPE brazil::City {
      CREATE REQUIRED PROPERTY ibge -> std::int32;
      CREATE REQUIRED PROPERTY name -> std::str;
  };
  CREATE SCALAR TYPE brazil::Acronyms EXTENDING enum<AC, AL, AP, AM, BA, CE, DF, ES, GO, MA, MT, MS, MG, PA, PB, PR, PE, PI, RJ, RN, RS, RO, RR, SC, SP, SE, TO>;
  CREATE TYPE brazil::State {
      CREATE REQUIRED PROPERTY acronym -> brazil::Acronyms;
      CREATE REQUIRED PROPERTY name -> std::str;
  };
  CREATE TYPE brazil::Address {
      CREATE MULTI LINK city -> brazil::City;
      CREATE MULTI LINK state -> brazil::State;
      CREATE REQUIRED PROPERTY zipcode -> std::int32 {
          CREATE CONSTRAINT std::exclusive;
          CREATE CONSTRAINT std::max_len_value(8);
      };
  };
};
