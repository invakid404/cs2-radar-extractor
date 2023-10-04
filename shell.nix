{ pkgs ? import <nixpkgs> {} }:

let
  pythonEnv = pkgs.python3.withPackages (ps: [
    ps.vpk
  ]);

  valveResourceFormat = import ./deps/vrf/default.nix {
    inherit pkgs;
  };
in
  pkgs.mkShell {
    buildInputs = [
      pythonEnv
      valveResourceFormat      
    ];
  }
