// Writes build-info.json for a release build: the plugin's first log line shows the release and
// commit it was built from. Run by "release:check" in the publish workflow (RELEASE_TAG is set).
import { writeFileSync } from 'node:fs';

const tag = process.env.RELEASE_TAG;
if (!tag) {
  console.error('build-info: RELEASE_TAG is not set; only release builds record build information');
  process.exit(1);
}
const { GITHUB_SHA = '', GITHUB_SERVER_URL = '', GITHUB_REPOSITORY = '', GITHUB_RUN_ID = '' } = process.env;
writeFileSync('build-info.json', JSON.stringify({
  tag,
  commit: GITHUB_SHA,
  built: new Date().toISOString(),
  run: `${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/actions/runs/${GITHUB_RUN_ID}`,
}, null, 2) + '\n');
console.log(`build-info.json: ${tag} ${GITHUB_SHA.slice(0, 7)}`);
