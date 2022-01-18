{ sources ? import ./sources.nix }:
import sources.nixpkgs {
  overlays = [
    (self: super: {
      python3Packages = super.python3.pkgs // {
        python-twitter-v2 = super.callPackage ./python-twitter-v2.nix {};
      };
    })
  ];
  config = {};
}
