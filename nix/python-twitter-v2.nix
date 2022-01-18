{ python3Packages }:

python3Packages.buildPythonPackage rec {
  pname = "python-twitter-v2";
  version = "0.7.2";

  src = python3Packages.fetchPypi {
    inherit pname version;
    sha256 = "0q1hsga2y1dab8qmsn137wl38ddgqfywyglv68pas0bqb7qldnpc";
  };

  propagatedBuildInputs = with python3Packages; [
    authlib
    dataclasses-json
    requests
  ];
}
