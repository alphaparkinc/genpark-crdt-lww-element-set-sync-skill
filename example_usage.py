from client import LWWElementSet

def run_example():
    print("=== GenPark CRDT LWW Element Set Example ===")
    crdt = LWWElementSet()
    crdt.add("peer-01", 10.0)
    crdt.add("peer-02", 20.0)
    crdt.remove("peer-01", 30.0)
    print("Current Elements:", crdt.elements())
    sync_res = crdt.merge_state({"peer-01": 40.0, "peer-03": 25.0}, {})
    print("After Monotonic Merge:", sync_res["converged_elements"])

if __name__ == "__main__":
    run_example()
