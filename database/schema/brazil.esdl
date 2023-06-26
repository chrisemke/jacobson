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
