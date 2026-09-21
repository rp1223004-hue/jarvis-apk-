name: Build JARVIS APK
on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install System Deps
        run: |
          sudo apt update
          sudo apt install -y openjdk-17-jdk zip unzip python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev libbz2-dev libsqlite3-dev libltdl-dev

      - name: Install Buildozer
        run: |
          pip install --upgrade pip
          pip install buildozer cython==0.29.36

      - name: Create License Files
        run: |
          mkdir -p ~/.android
          touch ~/.android/repositories.cfg
          mkdir -p ~/.android/licenses
          echo "8933bad161af4178b1185d1a37fbf41ea5269c55" > ~/.android/licenses/android-sdk-license
          echo "d56f5187479451eabf01fb78af6dfcb131a6481e" >> ~/.android/licenses/android-sdk-license
          echo "24333f8a63b6825ea9c5514f83c1059b8ea731" >> ~/.android/licenses/android-sdk-license
          echo "y" > /tmp/answer

      - name: Build APK First Run
        run: |
          yes | buildozer -v android debug || true

      - name: Accept All Licenses
        run: |
          SDK_MGR=$(find ~/.buildozer -name sdkmanager | head -n 1)
          echo "SDK Manager: $SDK_MGR"
          if [ -f "$SDK_MGR" ]; then
            yes | $SDK_MGR --licenses || true
            LICENSE_DIR=$(dirname "$SDK_MGR")/../../licenses
            mkdir -p "$LICENSE_DIR"
            cp ~/.android/licenses/android-sdk-license "$LICENSE_DIR/" || true
            ls -la "$LICENSE_DIR/" || true
          fi
          find ~/.buildozer -name "android-sdk-license" -exec cat {} \; || true

      - name: Build APK Final
        run: |
          buildozer -v android debug

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: JARVIS-APK
          path: bin/*.apk
          if-no-files-found: error
