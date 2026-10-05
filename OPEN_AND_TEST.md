# Open and test the DSA Study workspace

Follow these steps from a fresh checkout. They use only local project files
until the optional catalog sync step.

1. Open a terminal at the project root.

   ```bash
   cd workspace/side_projects/dsa_study
   ```

2. Create the isolated Python environment and install the project.

   ```bash
   python3 -m venv .venv
   .venv/bin/python -m pip install -e . pytest
   ```

3. Run deterministic tests. This verifies catalog normalization, HTML safety,
   private review data, authored-block requirements, visual controls, and the
   loopback execution API.

   ```bash
   .venv/bin/python -m pytest -p no:cacheprovider -q
   ```

4. Build the local study site. A previous local sync is required only when
   `data/catalog.json` is absent.

   ```bash
   dsa-study build
   # Optional; contacts the public provider and writes ignored generated data.
   # dsa-study sync
   ```

   When a local catalog exists, inspect non-sensitive coverage counts before
   using its generated problem pages:

   ```bash
   dsa-study audit
   ```

5. Start the local viewer. It binds only to your machine.

   ```bash
   dsa-study serve
   ```

6. Open `http://127.0.0.1:8765/`. Confirm that Guided study appears first,
   block selection changes the visible block, trace controls update the current
   state, curriculum context and the four pre-code fields appear before
   independent practice, and any bridge card stays concise. Confirm answer text
   is not retained after a reload and no personal answer is shown in catalog
   pages.

7. In another terminal, test the local runner with a trusted minimal request.

   ```bash
   curl -sS http://127.0.0.1:8765/api/run \
     -H 'Content-Type: application/json' \
     --data '{"code":"class Solution:\n    def add(self, a, b):\n        return a + b\n","method":"add","cases":[{"args":[2,3],"expected":5}]}'
   ```

   The expected result contains `"status": "accepted"`. The runner is not a
   security sandbox: submit only code you trust.

8. Stop the viewer with `Ctrl+C`. Check source formatting and project
   governance before handing work off.

   ```bash
   git diff --check
   cd ../../..
   python3 registry/implementation/cli.py validate
   python3 registry/implementation/cli.py build
   ```

Do not commit `data/`, `site/`, `.dsa-study/`, or `solutions/`. Their contents
can include imported material or Personal study work.
