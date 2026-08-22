// HUMAN Topic Demand Experiment v1 analytics destinations.
// Configure at least one destination before sending real experiment traffic.
// No destination is enabled by default, so development/preview traffic is not collected accidentally.
window.HUMAN_ANALYTICS = {
  experiment: 'topic-demand-v1',

  // Google Analytics 4: paste the Web stream Measurement ID, e.g. 'G-ABC123XYZ9'.
  // A Measurement ID is public website configuration. Never put API secrets or exports here.
  measurementId: 'G-HK2SR90C03',

  // Plausible: set to the registered production hostname, e.g. 'example.com'.
  plausibleDomain: '',
  plausibleScript: 'https://plausible.io/js/script.js',

  // Optional first-party/custom collector accepting JSON POST requests.
  endpoint: '',
  endpointMode: 'cors',

  // Can also be enabled per page with ?debug_analytics=1.
  debug: false,
};
