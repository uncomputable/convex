{ python3
, lib
}:
python3.pkgs.buildPythonApplication {
  pname = "convex";
  version = "0.1";

  src = ./.;

  meta = with lib; {
    description = "Convert between different hex representations";
    license = licenses.cc0;
  };
}
