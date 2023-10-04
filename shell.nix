{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = import ./common.nix {
    inherit pkgs;
  };
}