# shell.nix
{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.git
    pkgs.git-lfs
    pkgs.python311
    pkgs.python311Packages.numpy
    pkgs.python311Packages.opencv4
  ];
}
