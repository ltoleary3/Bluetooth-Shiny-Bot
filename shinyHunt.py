import nbxt

closeGame = """
HOME 0.1s
0.5s
X 0.1s
0.5s
A 0.1s
"""

startGame = """
A 0.1s
2.0s
B 0.1s
"""

if __name__ == "__main__":
    # Start NXBT
    nx = nxbt.Nxbt()

    # Get list of all Bluetooth adapters
    print("Getting bluetooth adapters")
    adapters = nx.get_available_adapters()
    controllerIndex = []

    # Create Pro Controller instance from all bluetooth adapters
    print("Creating Pro Controller instances")
    for i in range (0,len(adapters)):
        index = nx.create_controller(
            nxbt.PRO_CCONTROLLER,
            adapter_path=adapters[i])
        controllerIndex.append(index)

    # Wait for connection to last controller instance
    print("Connecting...")
    nx.wait_for_connection(controllerIndex[-1])
    print("Connected")

    # Start game macro
    nx.macro(controllerIndex, startGame)