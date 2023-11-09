let
  pkgs = import <nixpkgs> {};
in
  with pkgs; callPackage ./convex.nix {}
