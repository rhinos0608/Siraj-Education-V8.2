// TEMPORARY FIX: Direct backend connection
window.SIRAJ_API_OVERRIDE = {
  API_BASE_URL: 'http://localhost:8000',
  WS_BASE_URL: 'ws://localhost:8000'
};

console.log('🔧 SIRAJ API Override Active - Direct backend connection enabled');
