from flask import Blueprint, jsonify, request, send_file, make_response
from src.models.laporan_model import Laporan, StatusPengerjaan, Kategori
from src.models.user_model import User
from src import db
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from functools import wraps
from io import BytesIO
from reportlab.pdfgen import canvas
from docx import Document

laporan = Blueprint('laporan', __name__)

def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except IntegrityError:
            db.session.rollback()
            return jsonify({
                'status': "error",
                'message': "Database integrity error occurred"
            }), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'status': "error",
                'message': str(e)
            }), 500
    return decorated_function

@laporan.route('/getAllLaporan', methods=["GET"])
@handle_errors
def get_all_laporan():
    try:
        status_filter = request.args.get('status')
        kategori_filter = request.args.get('kategori')
        
        query = Laporan.query
        
        # Apply filters if they exist
        if status_filter:
            query = query.filter_by(status_pengerjaan=StatusPengerjaan(status_filter))
        if kategori_filter:
            query = query.filter_by(kategori=Kategori(kategori_filter))
        
        laporan_list = query.order_by(Laporan.created_at.desc()).all()
        
        if not laporan_list:
            return jsonify({
                'status': "success",
                'message': "Tidak ada laporan ditemukan.",
                'data': []
            }), 200
            
        return jsonify({
            'status': "success",
            'data': [laporan.to_dict() for laporan in laporan_list]
        }), 200
    except ValueError as e:
        return jsonify({
            'status': "error",
            'message': "Status atau kategori tidak valid"
        }), 400
    except Exception as e:
        return jsonify({
            'status': "error",
            'message': str(e)
        }), 500

@laporan.route('/getLaporanDetail/<int:id>', methods=["GET"])
@handle_errors
def get_laporan_detail(id):
    try:
        laporan = Laporan.query.get(id)
        if not laporan:
            return jsonify({
                'status': "error",
                'message': "Laporan tidak ditemukan."
            }), 404
            
        return jsonify({
            'status': "success",
            'data': laporan.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'status': "error",
            'message': str(e)
        }), 500

@laporan.route('/createLaporan', methods=["POST"])
@handle_errors
def create_laporan():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['judul_laporan', 'deskripsi', 'estimasi', 'kategori', 'id_user']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'status': "error",
                    'message': f"Field {field} harus diisi!"
                }), 400
        
        try:
            kategori = Kategori(data['kategori'])
        except ValueError:
            return jsonify({
                'status': "error",
                'message': "Kategori tidak valid. Pilih antara KERAMAIAN atau TUMPUKAN_SAMPAH"
            }), 400
                
        new_laporan = Laporan(
            judul_laporan=data['judul_laporan'],
            deskripsi=data['deskripsi'],
            estimasi=data['estimasi'],
            kategori=kategori,
            status_pengerjaan=StatusPengerjaan.BARU,
            id_user=data['id_user']
        )
        
        db.session.add(new_laporan)
        db.session.commit()
        
        return jsonify({
            'status': "success",
            'message': "Laporan berhasil dibuat.",
            'data': new_laporan.to_dict()
        }), 201
    except Exception as e:
        return jsonify({
            'status': "error",
            'message': str(e)
        }), 500

@laporan.route('/updateLaporan/<int:id>', methods=["PUT"])
@handle_errors
def update_laporan(id):
    try:
        laporan = Laporan.query.get(id)
        if not laporan:
            return jsonify({
                'status': "error",
                'message': "Laporan tidak ditemukan."
            }), 404
            
        data = request.get_json()
        
        # Update fields if they exist in request
        if 'judul_laporan' in data:
            laporan.judul_laporan = data['judul_laporan']
        if 'deskripsi' in data:
            laporan.deskripsi = data['deskripsi']
        if 'estimasi' in data:
            laporan.estimasi = data['estimasi']
        if 'kategori' in data:
            try:
                laporan.kategori = Kategori(data['kategori'])
            except ValueError:
                return jsonify({
                    'status': "error",
                    'message': "Kategori tidak valid. Pilih antara KERAMAIAN atau TUMPUKAN_SAMPAH"
                }), 400
        if 'status_pengerjaan' in data:
            try:
                laporan.status_pengerjaan = StatusPengerjaan(data['status_pengerjaan'])
            except ValueError:
                return jsonify({
                    'status': "error",
                    'message': "Status tidak valid. Pilih antara BARU, DIBACA, atau SELESAI"
                }), 400
            
        db.session.commit()
        
        return jsonify({
            'status': "success",
            'message': "Laporan berhasil diperbarui.",
            'data': laporan.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'status': "error",
            'message': str(e)
        }), 500

@laporan.route('/deleteLaporan/<int:id>', methods=["DELETE"])
@handle_errors
def delete_laporan(id):
    try:
        laporan = Laporan.query.get(id)
        if not laporan:
            return jsonify({
                'status': "error",
                'message': "Laporan tidak ditemukan."
            }), 404
            
        db.session.delete(laporan)
        db.session.commit()
        
        return jsonify({
            'status': "success",
            'message': "Laporan berhasil dihapus."
        }), 200
    except Exception as e:
        return jsonify({
            'status': "error",
            'message': str(e)
        }), 500


@laporan.route('/updateStatusLaporan/<int:id>', methods=["PATCH"])
@handle_errors
def update_status_laporan(id):
    """Endpoint khusus untuk mengubah status laporan"""
    try:
        laporan = Laporan.query.get(id)
        if not laporan:
            return jsonify({
                'status': "error",
                'message': "Laporan tidak ditemukan."
            }), 404
            
        data = request.get_json()
        
        if 'status_pengerjaan' not in data:
            return jsonify({
                'status': "error",
                'message': "Field status_pengerjaan harus diisi!"
            }), 400
            
        try:
            new_status = StatusPengerjaan(data['status_pengerjaan'])
            laporan.status_pengerjaan = new_status
            db.session.commit()
            
            return jsonify({
                'status': "success",
                'message': "Status berhasil diperbarui.",
                'data': {
                    'id': laporan.id,
                    'status_pengerjaan': laporan.status_pengerjaan.value
                }
            }), 200
        except ValueError:
            return jsonify({
                'status': "error",
                'message': "Status tidak valid. Pilih antara BARU, DIBACA, atau SELESAI"
            }), 400
    except Exception as e:
        return jsonify({
            'status': "error",
            'message': str(e)
        }), 500

@laporan.route('/downloadLaporan/<int:id>/<format>', methods=["GET"])
@handle_errors
def download_laporan(id, format):
    """Endpoint untuk mengunduh laporan dalam format PDF atau DOCX"""
    try:
        laporan = Laporan.query.get(id)
        if not laporan:
            return jsonify({
                'status': "error",
                'message': "Laporan tidak ditemukan."
            }), 404
            
        if format not in ['pdf', 'docx']:
            return jsonify({
                'status': "error",
                'message': "Format tidak valid. Pilih antara pdf atau docx"
            }), 400
            
        if format == 'pdf':
            # Create PDF
            buffer = BytesIO()
            p = canvas.Canvas(buffer)
            
            # Add document content
            p.drawString(100, 800, f"Judul Laporan: {laporan.judul_laporan}")
            p.drawString(100, 780, f"Jenis Laporan: {laporan.kategori.value}")
            p.drawString(100, 760, f"Status: {laporan.status_pengerjaan.value}")
            p.drawString(100, 740, f"Tanggal: {laporan.created_at.strftime('%Y-%m-%d %H:%M')}")
            p.drawString(100, 700, "Deskripsi:")
            text = p.beginText(100, 680)
            text.textLines(laporan.deskripsi)
            p.drawText(text)
            
            p.showPage()
            p.save()
            
            buffer.seek(0)
            response = make_response(buffer.getvalue())
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = f'attachment; filename=laporan_{id}.pdf'
            return response
            
        elif format == 'docx':
            # Create DOCX
            document = Document()
            document.add_heading(f'Laporan #{laporan.id}', 0)
            
            document.add_paragraph(f"Judul Laporan: {laporan.judul_laporan}")
            document.add_paragraph(f"Jenis Laporan: {laporan.kategori.value}")
            document.add_paragraph(f"Status: {laporan.status_pengerjaan.value}")
            document.add_paragraph(f"Tanggal: {laporan.created_at.strftime('%Y-%m-%d %H:%M')}")
            document.add_paragraph("Deskripsi:")
            document.add_paragraph(laporan.deskripsi)
            
            buffer = BytesIO()
            document.save(buffer)
            buffer.seek(0)
            
            response = make_response(buffer.getvalue())
            response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            response.headers['Content-Disposition'] = f'attachment; filename=laporan_{id}.docx'
            return response
            
    except Exception as e:
        return jsonify({
            'status': "error",
            'message': f"Gagal mengunduh laporan. Silakan coba lagi. Error: {str(e)}"
        }), 500