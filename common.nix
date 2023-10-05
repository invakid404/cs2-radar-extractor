{ pkgs ? import <nixpkgs> {} }:

let
  pythonEnv = pkgs.python3.withPackages (ps: [
    ps.vpk
    ps.vdf
    ps.pillow
    ps.sortedcollections
  ]);

  valveResourceFormat = import ./deps/vrf/default.nix {
    inherit pkgs;
  };
in [
  pythonEnv
  valveResourceFormat
]
