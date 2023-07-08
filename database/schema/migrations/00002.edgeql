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

CREATE MIGRATION m1yiks6kwrt6w7lxmtzfrvv7rkphbvqojwiwtirkqbihzbghtveniq
    ONTO m1t5im7wi6t5m6pnffk3glbeow6g425rrs6oamplfrrzsa3tnr42ba
{
  ALTER TYPE brazil::State {
      ALTER PROPERTY acronym {
          CREATE CONSTRAINT std::exclusive;
      };
      ALTER PROPERTY name {
          CREATE CONSTRAINT std::exclusive;
      };
  };
};
