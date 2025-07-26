#!/usr/bin/env python3
"""
SIRAJ Multi-Instance Test Script
================================

Quick test to verify multi-instance routing is working correctly.
"""

import asyncio
import httpx
import json
from datetime import datetime

# Configuration
ROUTER_URL = "http://localhost:5000"
ARCHETYPES = ['socratic', 'constructivist', 'storyteller', 'synthesizer', 'challenger', 'mentor', 'analyst']

async def test_router_health():
    """Test if router is healthy"""
    print("🔍 Testing router health...")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{ROUTER_URL}/api/health")
            data = response.json()
            
            print(f"✅ Router status: {data['status']}")
            print("\nInstance Status:")
            for name, info in data['instances'].items():
                print(f"  {name}: {'✅ Healthy' if info['healthy'] else '❌ Unhealthy'}")
                
            return data['status'] == 'healthy'
            
        except Exception as e:
            print(f"❌ Router health check failed: {e}")
            return False

async def test_archetype_routing():
    """Test archetype-specific routing"""
    print("\n🎭 Testing archetype routing...")
    
    question = "What is the meaning of learning?"
    results = {}
    
    async with httpx.AsyncClient() as client:
        for archetype in ARCHETYPES:
            print(f"\n  Testing {archetype}...", end='', flush=True)
            
            try:
                start = datetime.now()
                response = await client.post(
                    f"{ROUTER_URL}/api/query",
                    json={
                        "prompt": f"As a {archetype} teacher, briefly explain: {question}",
                        "archetype": archetype
                    },
                    timeout=30.0
                )
                
                elapsed = (datetime.now() - start).total_seconds()
                data = response.json()
                
                results[archetype] = {
                    'instance': data.get('instance'),
                    'response_length': len(data.get('response', '')),
                    'time': elapsed,
                    'success': True
                }
                
                print(f" ✅ {data.get('instance')} ({elapsed:.1f}s)")
                
            except Exception as e:
                print(f" ❌ Failed: {e}")
                results[archetype] = {
                    'error': str(e),
                    'success': False
                }
                
    return results

async def test_parallel_performance():
    """Test parallel vs sequential performance"""
    print("\n⚡ Testing parallel performance...")
    
    question = "Explain photosynthesis"
    
    async with httpx.AsyncClient() as client:
        # Sequential test
        print("\n  Sequential requests:")
        sequential_start = datetime.now()
        
        for i, archetype in enumerate(ARCHETYPES[:3]):
            response = await client.post(
                f"{ROUTER_URL}/api/query",
                json={
                    "prompt": f"As a {archetype}, explain: {question}",
                    "archetype": archetype
                },
                timeout=30.0
            )
            print(f"    {i+1}. {archetype} complete")
            
        sequential_time = (datetime.now() - sequential_start).total_seconds()
        print(f"  Sequential time: {sequential_time:.1f}s")
        
        # Parallel test
        print("\n  Parallel requests:")
        parallel_start = datetime.now()
        
        tasks = []
        for archetype in ARCHETYPES[:3]:
            task = client.post(
                f"{ROUTER_URL}/api/query",
                json={
                    "prompt": f"As a {archetype}, explain: {question}",
                    "archetype": archetype
                },
                timeout=30.0
            )
            tasks.append(task)
            
        responses = await asyncio.gather(*tasks)
        parallel_time = (datetime.now() - parallel_start).total_seconds()
        
        print(f"  Parallel time: {parallel_time:.1f}s")
        print(f"\n  🚀 Speedup: {sequential_time/parallel_time:.1f}x faster!")

async def test_failover():
    """Test failover capability"""
    print("\n🛡️ Testing failover (this will attempt 10 rapid requests)...")
    
    success_count = 0
    instance_count = {'A': 0, 'B': 0}
    
    async with httpx.AsyncClient() as client:
        for i in range(10):
            try:
                response = await client.post(
                    f"{ROUTER_URL}/api/query",
                    json={
                        "prompt": f"Quick test {i}",
                        "archetype": None  # Use round-robin
                    },
                    timeout=5.0
                )
                
                data = response.json()
                instance = data.get('instance', '').split('_')[-1]
                instance_count[instance] = instance_count.get(instance, 0) + 1
                success_count += 1
                
            except:
                pass
                
    print(f"  Success rate: {success_count}/10 ({success_count*10}%)")
    print(f"  Distribution: A={instance_count.get('A', 0)}, B={instance_count.get('B', 0)}")

async def main():
    """Run all tests"""
    print("=" * 60)
    print("SIRAJ Multi-Instance Test Suite")
    print("=" * 60)
    
    # Check if router is running
    try:
        if not await test_router_health():
            print("\n❌ Router is not running!")
            print("Please start the launcher first: python launcher.py")
            return
    except:
        print("\n❌ Cannot connect to router!")
        print("Please start the launcher first: python launcher.py")
        return
        
    # Run tests
    results = await test_archetype_routing()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    instance_a = sum(1 for r in results.values() if r.get('instance') == 'Gemma_Instance_A')
    instance_b = sum(1 for r in results.values() if r.get('instance') == 'Gemma_Instance_B')
    success_count = sum(1 for r in results.values() if r.get('success'))
    
    print(f"\n✅ Success rate: {success_count}/{len(ARCHETYPES)} archetypes")
    print(f"📊 Instance distribution: A={instance_a}, B={instance_b}")
    
    # Verify correct mapping
    print("\n🔍 Verifying archetype mapping:")
    expected_a = ['socratic', 'constructivist', 'storyteller']
    expected_b = ['synthesizer', 'challenger', 'mentor', 'analyst']
    
    correct_mapping = True
    for arch in expected_a:
        if results.get(arch, {}).get('instance') != 'Gemma_Instance_A':
            print(f"  ❌ {arch} should be on Instance A")
            correct_mapping = False
            
    for arch in expected_b:
        if results.get(arch, {}).get('instance') != 'Gemma_Instance_B':
            print(f"  ❌ {arch} should be on Instance B")
            correct_mapping = False
            
    if correct_mapping:
        print("  ✅ All archetypes correctly mapped!")
        
    # Performance test
    await test_parallel_performance()
    
    # Failover test
    await test_failover()
    
    print("\n✨ Test complete!")

if __name__ == "__main__":
    asyncio.run(main())
