{ pkgs ? import ./nix/nixpkgs.nix {} }:

pkgs.mkShell {
  name = "twitter-wordle";
  buildInputs = [
    pkgs.python3Packages.python-twitter-v2
  ];
}
