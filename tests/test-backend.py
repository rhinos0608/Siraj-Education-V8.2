#!/usr/bin/env python3
"""
Quick Backend Test Script
========================
Test if the backend is running and responding correctly
"""

import asyncio
import json
import httpx

async def test_backend():
    """Test backend endpoints"""
    print("🔍 Testing SIRAJ Educational AI Backend...")
    
    base_url = "http://localhost:8000"
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Test 1: Health check
            print("\n1. Testing health endpoint...")
            try:
                response = await client.get(f"{base_url}/health")
                print(f"   Status: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"   Health: {data.get('status', 'unknown')}")
                    print(f"   Ollama: {data.get('ollama_connected', False)}")
                    print(f"   Fallback mode: {data.get('fallback_mode', True)}")
                else:
                    print(f"   Error: {response.text}")
            except Exception as e:
                print(f"   Failed: {e}")
            
            # Test 2: Educational query endpoint
            print("\n2. Testing educational query endpoint...")
            test_request = {
                "topic": "What is photosynthesis?",
                "grade_level": "middle",
                "selected_archetypes": ["socratic", "mentor"]
            }
            
            try:
                response = await client.post(
                    f"{base_url}/api/education/query",
                    json=test_request
                )
                print(f"   Status: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"   Session ID: {data.get('session_id', 'none')}")
                    print(f"   Topic: {data.get('topic', 'none')}")
                    print(f"   Degraded mode: {data.get('degraded_mode', True)}")
                    print(f"   Council responses: {len(data.get('council_responses', {}))}")
                    print("   ✅ Educational query endpoint working!")
                else:
                    print(f"   Error: {response.status_code} - {response.text}")
            except Exception as e:
                print(f"   Failed: {e}")
            
            # Test 3: Archetypes endpoint
            print("\n3. Testing archetypes endpoint...")
            try:
                response = await client.get(f"{base_url}/council/archetypes")
                print(f"   Status: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"   Archetypes count: {data.get('count', 0)}")
                    print("   ✅ Archetypes endpoint working!")
                else:
                    print(f"   Error: {response.text}")
            except Exception as e:
                print(f"   Failed: {e}")
                
    except Exception as e:
        print(f"❌ Backend connection failed: {e}")
        print("\n🔧 Troubleshooting steps:")
        print("1. Make sure the backend is running: python backend/main.py")
        print("2. Check if port 8000 is available")
        print("3. Verify no firewall blocking localhost connections")
        return False
        
    print(f"\n✅ Backend test complete!")
    return True

if __name__ == "__main__":
    asyncio.run(test_backend())
