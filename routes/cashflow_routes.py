from flask import Blueprint, render_template, redirect, url_for, flash, request
# from flask_login import login_required, current_user # Hapus impor ini
from models.cashflow import CashFlow
from extensions import db
from forms.cashflow_forms import CashFlowForm

cashflow_bp = Blueprint('cashflow', __name__)

@cashflow_bp.route('/cashflow')
def index():
    cashflows = CashFlow.query.order_by(CashFlow.date.desc()).all()
    saldo = 0
    for c in CashFlow.query.order_by(CashFlow.date, CashFlow.id).all():
        if c.type == 'income':
            saldo += c.amount
        else:
            saldo -= c.amount
    return render_template('cashflow/index.html', cashflows=cashflows, saldo=saldo)

@cashflow_bp.route('/cashflow/add', methods=['GET', 'POST'])
# @login_required # Hapus dekorator ini
def add():
    # if not current_user.is_admin: # Hapus atau ubah logika ini
    #     flash('Hanya admin yang dapat menambah data cashflow.', 'danger')
    #     return redirect(url_for('cashflow.index'))
    form = CashFlowForm()
    if form.validate_on_submit():
        cashflow = CashFlow(
            date=form.date.data,
            type=form.type.data,
            amount=form.amount.data,
            description=form.description.data
        )
        db.session.add(cashflow)
        db.session.commit()
        flash('Data cashflow berhasil ditambahkan.', 'success')
        return redirect(url_for('cashflow.index'))
    return render_template('cashflow/add.html', form=form)

@cashflow_bp.route('/cashflow/edit/<int:id>', methods=['GET', 'POST'])
# @login_required # Hapus dekorator ini
def edit(id):
    # if not current_user.is_admin: # Hapus atau ubah logika ini
    #     flash('Hanya admin yang dapat mengedit data cashflow.', 'danger')
    #     return redirect(url_for('cashflow.index'))
    cashflow = CashFlow.query.get_or_404(id)
    form = CashFlowForm(obj=cashflow)
    if form.validate_on_submit():
        cashflow.date = form.date.data
        cashflow.type = form.type.data
        cashflow.amount = form.amount.data
        cashflow.description = form.description.data
        db.session.commit()
        flash('Data cashflow berhasil diupdate.', 'success')
        return redirect(url_for('cashflow.index'))
    return render_template('cashflow/edit.html', form=form, cashflow=cashflow)

@cashflow_bp.route('/cashflow/delete/<int:id>', methods=['POST'])
# @login_required # Hapus dekorator ini
def delete(id):
    # if not current_user.is_admin: # Hapus atau ubah logika ini
    #     flash('Hanya admin yang dapat menghapus data cashflow.', 'danger')
    #     return redirect(url_for('cashflow.index'))
    cashflow = CashFlow.query.get_or_404(id)
    db.session.delete(cashflow)
    db.session.commit()
    flash('Data cashflow berhasil dihapus.', 'success')
    return redirect(url_for('cashflow.index'))
