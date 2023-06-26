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
