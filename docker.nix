{ pkgs ? import <nixpkgs> {} }:

let
  inputs = import ./common.nix {
    inherit pkgs;
  };
  entrypoint = pkgs.writeTextDir "bin/extract.py" (builtins.readFile ./extract.py);
in
  pkgs.dockerTools.buildImage {
    name = "ghcr.io/invakid404/cs2-radar-extractor";
    tag = "latest";
    copyToRoot = pkgs.buildEnv {
      name = "image-root";
      pathsToLink = [ "/" ];
      paths = inputs ++ [
        entrypoint
      ];
    };
    config = {
      Cmd = [ "/bin/python3" "/bin/extract.py" ];
      WorkingDir = "/data";
      Env = [
        "CS2_PATH=/cs2"
      ];
    };
  }
