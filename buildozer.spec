
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
