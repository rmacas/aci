from master_agent import MasterAgent
import json
import matplotlib.pyplot as plt


def plot_responses(question, aggregated_response):
    """Create a bar plot of Yes/No responses."""
    # Check if we have an error response
    if 'error' in aggregated_response:
        print(f"\nError: {aggregated_response['error']}")
        if 'error_details' in aggregated_response:
            print(f"Details: {aggregated_response['error_details']}")
        return

    # Extract data
    yes_count = aggregated_response['yes_count']
    no_count = aggregated_response['no_count']

    # Create the plot
    plt.figure(figsize=(10, 6))
    bars = plt.bar(['Yes', 'No'], [yes_count, no_count],
                   color=['green', 'red'])

    # Add count labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{int(height)}',
                 ha='center', va='bottom')

    # Customize the plot
    plt.title(f'{question}', pad=20)
    plt.ylabel('Number of Responses')
    plt.ylim(0, max(yes_count, no_count) * 1.2)  # Add 20% padding

    # Add percentage labels
    plt.text(0, yes_count/2, f'{aggregated_response["yes_percentage"]:.1f}%',
             ha='center', va='center', color='white', fontweight='bold')
    plt.text(1, no_count/2, f'{aggregated_response["no_percentage"]:.1f}%',
             ha='center', va='center', color='white', fontweight='bold')

    plt.tight_layout()
    plt.savefig('response.png', dpi=200, bbox_inches='tight')
    plt.close()


def main():
    print("Welcome to the Artificial Crowd Intelligence System!")

    # Get number of personas from user
    while True:
        try:
            prompt = "\nEnter the number of personas to simulate (1-100): "
            num_personas = int(input(prompt))
            if 1 <= num_personas <= 100:
                break
            print("Please enter a number between 1 and 100.")
        except ValueError:
            print("Please enter a valid number.")

    # Initialize the master agent with user-specified number of personas
    master = MasterAgent(num_personas=num_personas)
    print("\nCurrent personas:")
    print(master)

    while True:
        print("\n" + "="*50)
        question = input("\nEnter your question (or 'quit' to exit): ")
        if question.lower() == 'quit':
            break
        print("\nGathering responses from personas...")
        result = master.get_crowd_response(question)

        print("\nIndividual Responses:")
        for response in result['individual_responses']:
            print(f"\n{response}")

        print("\nAggregated Response:")
        if isinstance(result['aggregated_response'], dict):
            print(json.dumps(result['aggregated_response'], indent=2))
            # Create and show the plot
            plot_responses(question, result['aggregated_response'])
        else:
            print(result['aggregated_response'])


if __name__ == "__main__":
    main()
