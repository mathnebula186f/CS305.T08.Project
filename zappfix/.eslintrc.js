module.exports = {
    root: true,
    extends: [
      'universe/native',
    ],
    rules: {
      // Ensures props and state inside functions are always up-to-date
        'react-hooks/exhaustive-deps': 'off',
        'prettier/prettier': 'off', 
        'no-unused-vars': 'off',
        'import/order': 'off',
        'object-shorthand': 'off',
        'prefer-const': 'off',
        'eqeqeq': 'off',
    },
  };
  