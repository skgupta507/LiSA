const { spawnSync } = require('child_process');
const spawnOptions = { detached: false, shell: true, stdio: 'inherit' };

/**
 * @namespace Builder
 * @description - Builds React & Python builds of project so Electron can be used.
 */
class Builder {
    /**
     * @description - Creates React and Python production builds.
     * @memberof Builder
     */
    buildAll = () => {
        const { buildPython, buildReact } = this;

        buildPython();
        buildReact();
    };

    /**
     * @description - Creates production build of Python back end.
     * @memberof Builder
     */
    buildPython = () => {
        console.log('Creating Python distribution files...');

        const app = 'backend/LiSA.py';
        const icon = './public/favicon.ico';

        const options = [
            '--noconfirm', // Don't confirm overwrite
            '--distpath ./resources', // Dist (out) path
            `--icon ${icon}`, // Icon to use
        ].join(' ');
        // TODO: Check if python is installed.. If not, prompt user
        // "Python is required but not installed, install it? (y/n)"
        spawnSync(`pyinstaller spec/windows.spec --clean`, spawnOptions);
    };

    /**
     * @description - Creates production build of React front end.
     * @memberof Builder
     */
    buildReact = () => {
        console.log('Creating React distribution files...');
        spawnSync(`tsc && vite build`, spawnOptions);
    };
}

module.exports.Builder = Builder;
