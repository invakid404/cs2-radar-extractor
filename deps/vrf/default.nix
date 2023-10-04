{ pkgs ? import <nixpkgs> { system = builtins.currentSystem; }
, fetchFromGitHub ? pkgs.fetchFromGitHub
, buildDotnetModule ? pkgs.buildDotnetModule
, dotnet-sdk_7 ? pkgs.dotnet-sdk_7
}:

buildDotnetModule rec {
  pname = "ValveResourceFormat";
  version = "5.0";

  src = fetchFromGitHub {
    owner = pname;
    repo = pname;
    rev = "5859d5e3f2c412fa89f96fa9bf1ae2585e65a4ee";
    sha256 = "sha256-Xdk+EztbfFZqnDO6sGFahcKxNCTpereFuxQSZERTuKU=";
  };

  nugetDeps = ./deps.nix;

  dotnet-runtime = dotnet-sdk_7;
  dotnet-sdk = dotnet-sdk_7;

  projectFile = "./Decompiler/Decompiler.csproj";
}
