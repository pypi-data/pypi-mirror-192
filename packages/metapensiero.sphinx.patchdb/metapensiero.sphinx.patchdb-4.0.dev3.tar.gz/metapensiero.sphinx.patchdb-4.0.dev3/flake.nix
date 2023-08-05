# -*- coding: utf-8 -*-
# :Project:   PatchDB — Development environment
# :Created:   dom 26 giu 2022, 11:48:09
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2022, 2023 Lele Gaifax
#

{
  description = "metapensiero.sphinx.patchdb";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };

        mkTestShell = python:
          let
            patchdb = python.pkgs.buildPythonApplication rec {
              name = "patchdb";
              src = ./.;
              buildInputs = [
                python.pkgs.flitBuildHook
              ];
              propagatedBuildInputs = [
                #docutils0171
              ] ++ (with python.pkgs; [
                enlighten
                sqlparse
              ]);
              buildPhase = "flitBuildPhase";
              doCheck = false;
            };

            psycopg = python.pkgs.buildPythonPackage rec {
              pname = "psycopg";
              version = "3.1.8";
              src = python.pkgs.fetchPypi {
                inherit pname version;
                hash = "sha256:59b4a71536b146925513c0234dfd1dc42b81e65d56ce5335dff4813434dbc113";
              };
              nativeBuildInputs = [
                pkgs.postgresql
                python.pkgs.typing-extensions
              ];
              doCheck = false;
            };
          in
            pkgs.mkShell {
              name = "Test Python ${python.version}";
              packages = [
                python
                patchdb
                psycopg
              ] ++ (with python.pkgs; [
                pytest
                docutils
                sphinx
                sqlparse
              ]);

              LANG="C";
            };
      in {
        devShells = {
          default = pkgs.mkShell {
            name = "Dev shell";

            packages = with pkgs; [
              bump2version
              gnumake
              python3
              twine
            ] ++ (with pkgs.python3Packages; [
              babel
              build
              tomli
            ]);

            shellHook = ''
               export PYTHONPATH="$(pwd)/src''${PYTHONPATH:+:}$PYTHONPATH"
             '';
          };

          testPy39 = mkTestShell pkgs.python39;
          testPy310 = mkTestShell pkgs.python310;
        };
      });
}
