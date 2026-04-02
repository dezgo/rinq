"""Run Rinq development server."""
from rinq.app import app, config

if __name__ == '__main__':
    print("\n" + "=" * 50)
    print(f"  {config.product_name} — {config.description}")
    print(f"  http://localhost:{config.server_port}")
    print("=" * 50 + "\n")

    app.run(
        host=config.server_host,
        port=config.server_port,
        debug=True,
    )
