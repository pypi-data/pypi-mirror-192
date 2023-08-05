// vetur.config.js
/** @type {import('vls').VeturConfig} */
module.exports = {
    settings: {
      "vetur.useWorkspaceDependencies": true,
      "vetur.experimental.templateInterpolationService": false,
    },
    projects: [
      {
        root: "./web",
        package: "./package.json",
      },
    ]
  };