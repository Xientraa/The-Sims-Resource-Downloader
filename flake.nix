{
  description = "Super simple rust library to display images in the terminal";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {self, nixpkgs, flake-utils}:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {inherit system;};
        pkgs-python = pkgs.python3.pkgs;

        clipboard = with pkgs-python; buildPythonPackage {
          pname = "clipboard";
          version = "0.0.4";
          src = fetchPypi {
            pname = "clipboard";
            version = "0.0.4";
            sha256 = "sha256-pyp46cm/aNocPynuAiQX0T7J44JLURVZ/StwKx3VuBc=";
          };
          propagatedBuildInputs = [pyperclip];
          doCheck = false;
          pyproject = true;
          build-system = [setuptools];
        };

        pythonEnv = pkgs.python3.withPackages (ps: [
          ps.requests
          ps.platformdirs
          clipboard
        ]);
        pname = "tsr-downloader";
        app = with pkgs-python; buildPythonApplication {
          inherit pname;
          version = "0.4.2";
          src = ./.;
          format = "other";
          installPhase = ''
            mkdir -p $out/lib/src
            cp -r src/* $out/lib/src

            makeWrapper ${pythonEnv}/bin/python $out/bin/${pname} \
              --prefix PATH : ${pkgs.wl-clipboard}/bin \
              --add-flags "$out/lib/src/main.py"
          '';
        };
      in {
        packages.default = app;

        apps.default = {
          type = "app";
          program = "${app}/bin/${pname}";
        };
      }
    );
}
