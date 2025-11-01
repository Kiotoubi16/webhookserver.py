from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Store signals in memory
signals = []
WEBHOOK_SECRET = "your_password_123"  # Change this!

@app.route('/webhook', methods=['POST'])
def webhook():
    """Receives signals from TradingView"""
    try:
        data = request.get_json()
        
        if data.get('secret') != WEBHOOK_SECRET:
            return jsonify({'error': 'Invalid secret'}), 403
        
        data['timestamp'] = datetime.now().isoformat()
        data['processed'] = False
        signals.append(data)
        
        print(f"Signal received: {data}")
        return jsonify({'status': 'success'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_signals', methods=['GET'])
def get_signals():
    """Your PC gets signals from here"""
    unprocessed = [s for s in signals if not s.get('processed')]
    return jsonify(unprocessed), 200

@app.route('/mark_processed/<int:index>', methods=['POST'])
def mark_processed(index):
    """Mark signal as done"""
    if index < len(signals):
        signals[index]['processed'] = True
        return jsonify({'status': 'success'}), 200
    return jsonify({'error': 'Invalid index'}), 404

@app.route('/health', methods=['GET'])
def health():
    """Check server status"""
    return jsonify({
        'status': 'running',
        'time': datetime.now().isoformat(),
        'total_signals': len(signals),
        'pending': len([s for s in signals if not s.get('processed')])
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
