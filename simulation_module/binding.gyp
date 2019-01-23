{
  'targets': [
    {
      'target_name': 'simulation_module-native',
      'sources': [ 'src/simulation_module.cc', 'src/command_parser.cc', 'src/simulation_settings.cc', 'src/simulation_world.cc', 'src/simulation_node.cc', 'src/simulation_graph.cc', 'src/simulation_participant.cc', 'src/simulation_data.cc'],
      'include_dirs': ["<!@(node -p \"require('node-addon-api').include\")", "lib/json/single_include/nlohmann"],
      'dependencies': ["<!(node -p \"require('node-addon-api').gyp\")"],
      'cflags!': [ '-fno-exceptions' ],
      'cflags_cc!': [ '-fno-exceptions' ],
      'xcode_settings': {
        'GCC_ENABLE_CPP_EXCEPTIONS': 'YES',
        'CLANG_CXX_LIBRARY': 'libc++',
        'MACOSX_DEPLOYMENT_TARGET': '10.7'
      },
      'msvs_settings': {
        'VCCLCompilerTool': { 'ExceptionHandling': 1 },
      }
    }
  ]
}