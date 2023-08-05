!
! Copyright (C) 2001-2013 Quantum ESPRESSO group
! This file is distributed under the terms of the
! GNU General Public License. See the file `License'
! in the root directory of the present distribution,
! or http://www.gnu.org/copyleft/gpl.txt .
!
!----------------------------------------------------------------------------
SUBROUTINE qepy_v_of_rho_all( rho, rho_core, rhog_core, &
                     ehart, etxc, vtxc, eth, etotefield, charge, v, embed)
  !----------------------------------------------------------------------------
  !! This routine computes the Hartree and Exchange and Correlation
  !! potential and energies which corresponds to a given charge density
  !! The XC potential is computed in real space, while the
  !! Hartree potential is computed in reciprocal space.
  !
  USE kinds,            ONLY : DP
  USE fft_base,         ONLY : dfftp
  USE gvect,            ONLY : ngm
  USE noncollin_module, ONLY : noncolin, nspin_lsda
  USE ions_base,        ONLY : nat, tau
  USE ldaU,             ONLY : lda_plus_U 
  USE funct,            ONLY : dft_is_meta, get_meta
  USE scf,              ONLY : scf_type
  USE cell_base,        ONLY : alat
  USE control_flags,    ONLY : ts_vdw
  USE tsvdw_module,     ONLY : tsvdw_calculate, UtsvdW
  USE scf,                  ONLY : vltot, vrs, kedtau, vnew
  USE gvecs,                ONLY : doublegrid
  USE lsda_mod,             ONLY : lsda, nspin, magtot, absmag, isk
  USE plugin_variables,     ONLY : plugin_etot
  USE dfunct,               ONLY : newd
  USE paw_variables,        ONLY : okpaw, ddd_paw, total_core_energy, only_paw
  USE paw_onecenter,        ONLY : PAW_potential
  USE paw_symmetry,         ONLY : PAW_symmetrize_ddd
  USE ener,                 ONLY : epaw
  !
  USE qepy_common,             ONLY : embed_base
  !
  IMPLICIT NONE
  !
  TYPE(embed_base), INTENT(INOUT)    :: embed
  !
  TYPE(scf_type), INTENT(INOUT) :: rho
  !! the valence charge
  TYPE(scf_type), INTENT(INOUT) :: v
  !! the scf (Hxc) potential 
  !=================> NB: NOTE that in F90 derived data type must be INOUT and 
  !=================> not just OUT because otherwise their allocatable or pointer
  !=================> components are NOT defined 
  REAL(DP), INTENT(IN) :: rho_core(dfftp%nnr)
  !! the core charge
  COMPLEX(DP), INTENT(IN) :: rhog_core(ngm)
  !! the core charge in reciprocal space
  REAL(DP), INTENT(OUT) :: vtxc
  !! the integral V_xc * rho
  REAL(DP), INTENT(OUT) :: etxc
  !! the E_xc energy
  REAL(DP), INTENT(OUT) :: ehart
  !! the hartree energy
  REAL(DP), INTENT(OUT) :: eth
  !! the hubbard energy
  REAL(DP), INTENT(OUT) :: charge
  !! the integral of the charge
  REAL(DP), INTENT(INOUT) :: etotefield
  !! electric field energy - inout due to the screwed logic of add_efield
  !
  INTEGER :: is, ir
  LOGICAL :: conv_elec
  REAL(DP) :: dr2
  REAL(DP) :: etot_cmp_paw(nat,2,2)

  call qepy_v_of_rho( rho, rho_core, rhog_core, &
                     ehart, etxc, vtxc, eth, etotefield, charge, v, embed)
  IF (okpaw) THEN
     CALL PAW_potential( rho%bec, ddd_paw, epaw, etot_cmp_paw )
     CALL PAW_symmetrize_ddd( ddd_paw )
  ENDIF

  CALL plugin_scf_energy(plugin_etot,rho)
  !
  CALL plugin_scf_potential(rho,conv_elec,dr2,vltot)
  !
  ! ... define the total local potential (external + scf)
  !
  CALL embed%allocate_extpot()
  v%of_r = v%of_r + embed%extpot
  !
  CALL sum_vrs( dfftp%nnr, nspin, vltot, v%of_r, vrs )
  !
  ! ... interpolate the total local potential
  !
  CALL interpolate_vrs( dfftp%nnr, nspin, doublegrid, kedtau, v%kin_r, vrs )
  !
  ! ... in the US case we have to recompute the self-consistent
  ! ... term in the nonlocal potential
  ! ... PAW: newd contains PAW updates of NL coefficients
  !
  CALL newd()
  END SUBROUTINE 
!----------------------------------------------------------------------------
SUBROUTINE qepy_v_of_rho( rho, rho_core, rhog_core, &
                     ehart, etxc, vtxc, eth, etotefield, charge, v, embed)
  !----------------------------------------------------------------------------
  !! This routine computes the Hartree and Exchange and Correlation
  !! potential and energies which corresponds to a given charge density
  !! The XC potential is computed in real space, while the
  !! Hartree potential is computed in reciprocal space.
  !
  USE kinds,            ONLY : DP
  USE fft_base,         ONLY : dfftp
  USE gvect,            ONLY : ngm
  USE noncollin_module, ONLY : noncolin, nspin_lsda
  USE ions_base,        ONLY : nat, tau
  USE ldaU,             ONLY : lda_plus_U 
  USE funct,            ONLY : dft_is_meta, get_meta
  USE scf,              ONLY : scf_type
  USE cell_base,        ONLY : alat
  USE control_flags,    ONLY : ts_vdw
  USE tsvdw_module,     ONLY : tsvdw_calculate, UtsvdW
  USE qepy_common,         ONLY : embed_base
  !
  IMPLICIT NONE
  !
  type(embed_base), intent(in)    :: embed
  !
  TYPE(scf_type), INTENT(INOUT) :: rho
  !! the valence charge
  TYPE(scf_type), INTENT(INOUT) :: v
  !! the scf (Hxc) potential 
  !=================> NB: NOTE that in F90 derived data type must be INOUT and 
  !=================> not just OUT because otherwise their allocatable or pointer
  !=================> components are NOT defined 
  REAL(DP), INTENT(IN) :: rho_core(dfftp%nnr)
  !! the core charge
  COMPLEX(DP), INTENT(IN) :: rhog_core(ngm)
  !! the core charge in reciprocal space
  REAL(DP), INTENT(OUT) :: vtxc
  !! the integral V_xc * rho
  REAL(DP), INTENT(OUT) :: etxc
  !! the E_xc energy
  REAL(DP), INTENT(OUT) :: ehart
  !! the hartree energy
  REAL(DP), INTENT(OUT) :: eth
  !! the hubbard energy
  REAL(DP), INTENT(OUT) :: charge
  !! the integral of the charge
  REAL(DP), INTENT(INOUT) :: etotefield
  !! electric field energy - inout due to the screwed logic of add_efield
  !
  INTEGER :: is, ir
  !
  CALL start_clock( 'v_of_rho' )
  !
  ! ... calculate exchange-correlation potential
  !
  if (iand(embed%exttype,4) == 0) then ! XC
  IF (dft_is_meta()) then
     CALL v_xc_meta( rho, rho_core, rhog_core, etxc, vtxc, v%of_r, v%kin_r )
  ELSE
     CALL v_xc( rho, rho_core, rhog_core, etxc, vtxc, v%of_r )
  ENDIF
  else
  v%of_r(:,:) = 0.0
  etxc = 0.0
  end if
  !
  ! ... add a magnetic field  (if any)
  !
  CALL add_bfield( v%of_r, rho%of_r )
  !
  ! ... calculate hartree potential
  !
  if (iand(embed%exttype,2) == 0) then ! Hartree
  CALL v_h( rho%of_g(:,1), ehart, charge, v%of_r )
  else
     ehart=0.0
  end if
  !
  ! ... LDA+U: build up Hubbard potential 
  !
  IF (lda_plus_u) then
     IF (noncolin) then
        CALL v_hubbard_nc(rho%ns_nc,v%ns_nc,eth)
     ELSE
        CALL v_hubbard(rho%ns,v%ns,eth)
     ENDIF
  ENDIF
  !
  ! ... add an electric field
  ! 
  DO is = 1, nspin_lsda
     CALL add_efield(v%of_r(1,is), etotefield, rho%of_r(:,1), .false. )
  END DO
  !
  ! ... add Tkatchenko-Scheffler potential (factor 2: Ha -> Ry)
  !
  IF (ts_vdw) THEN
     CALL tsvdw_calculate(tau*alat,rho%of_r(:,1))
     DO is = 1, nspin_lsda
        DO ir=1,dfftp%nnr
           v%of_r(ir,is)=v%of_r(ir,is)+2.0d0*UtsvdW(ir)
        END DO
     END DO
  END IF
  !
  CALL stop_clock( 'v_of_rho' )
  !
  RETURN
  !
END SUBROUTINE qepy_v_of_rho
!
!
!----------------------------------------------------------------------------
!SUBROUTINE v_xc_meta( rho, rho_core, rhog_core, etxc, vtxc, v, kedtaur )
  !!----------------------------------------------------------------------------
  !!! Exchange-Correlation potential (meta) Vxc(r) from n(r)
  !!
  !USE kinds,            ONLY : DP
  !USE constants,        ONLY : e2, eps8
  !USE io_global,        ONLY : stdout
  !USE fft_base,         ONLY : dfftp
  !USE gvect,            ONLY : g, ngm
  !USE lsda_mod,         ONLY : nspin
  !USE cell_base,        ONLY : omega
  !USE funct,            ONLY : get_meta, dft_is_nonlocc, nlc, is_libxc
  !USE xc_mgga,          ONLY : xc_metagcx
  !USE scf,              ONLY : scf_type, rhoz_or_updw
  !USE mp,               ONLY : mp_sum
  !USE mp_bands,         ONLY : intra_bgrp_comm
  !!
  !IMPLICIT NONE
  !!
  !TYPE (scf_type), INTENT(INOUT) :: rho
  !!! the valence charge
  !REAL(DP), INTENT(IN) :: rho_core(dfftp%nnr)
  !!! the core charge in real space
  !COMPLEX(DP), INTENT(IN) :: rhog_core(ngm)
  !!! the core charge in reciprocal space
  !REAL(DP), INTENT(INOUT) :: v(dfftp%nnr,nspin)
  !!! V_xc potential
  !REAL(DP), INTENT(INOUT) :: kedtaur(dfftp%nnr,nspin)
  !!! local K energy density                     
  !REAL(DP), INTENT(INOUT) :: vtxc
  !!! integral V_xc * rho
  !REAL(DP), INTENT(INOUT) :: etxc
  !!! E_xc energy
  !!
  !! ... local variables
  !!
  !REAL(DP) :: zeta, rh, sgn(2)
  !INTEGER  :: k, ipol, is, np
  !!
  !REAL(DP), ALLOCATABLE :: ex(:), ec(:)
  !REAL(DP), ALLOCATABLE :: v1x(:,:), v2x(:,:), v3x(:,:)
  !REAL(DP), ALLOCATABLE :: v1c(:,:), v2c(:,:,:), v3c(:,:)
  !!
  !REAL(DP) :: fac
       
  !REAL(DP), DIMENSION(2) :: grho2, rhoneg
  !REAL(DP), DIMENSION(3) :: grhoup, grhodw
  !!
  !REAL(DP), ALLOCATABLE :: grho(:,:,:), h(:,:,:), dh(:)
  !REAL(DP), ALLOCATABLE :: rhoout(:)
  !COMPLEX(DP), ALLOCATABLE :: rhogsum(:)
  !REAL(DP), PARAMETER :: eps12 = 1.0d-12, zero=0._dp
  !!
  !CALL start_clock( 'v_xc_meta' )
  !!
  !etxc = zero
  !vtxc = zero
  !v(:,:) = zero
  !rhoneg(:) = zero
  !sgn(1) = 1._dp  ;   sgn(2) = -1._dp
  !fac = 1.D0 / DBLE( nspin )
  !np = 1
  !IF (nspin==2) np=3
  !!
  !ALLOCATE( grho(3,dfftp%nnr,nspin) )
  !ALLOCATE( h(3,dfftp%nnr,nspin) )
  !ALLOCATE( rhogsum(ngm) )
  !!
  !ALLOCATE( ex(dfftp%nnr), ec(dfftp%nnr) )
  !ALLOCATE( v1x(dfftp%nnr,nspin), v2x(dfftp%nnr,nspin)   , v3x(dfftp%nnr,nspin) )
  !ALLOCATE( v1c(dfftp%nnr,nspin), v2c(np,dfftp%nnr,nspin), v3c(dfftp%nnr,nspin) )
  !!
  !! ... calculate the gradient of rho + rho_core in real space
  !! ... in LSDA case rhogsum is in (up,down) format
  !!
  !DO is = 1, nspin
     !!
     !rhogsum(:) = fac*rhog_core(:) + ( rho%of_g(:,1) + sgn(is)*rho%of_g(:,nspin) )*0.5D0
     !!
     !CALL fft_gradient_g2r( dfftp, rhogsum, g, grho(1,1,is) )
     !!
  !ENDDO
  !DEALLOCATE(rhogsum)
  !!
  !!
  !IF (nspin == 1) THEN
    !!
    !CALL xc_metagcx( dfftp%nnr, 1, np, rho%of_r, grho, rho%kin_r/e2, ex, ec, &
                      !v1x, v2x, v3x, v1c, v2c, v3c )
    !!
    !DO k = 1, dfftp%nnr
       !!
       !v(k,1) = (v1x(k,1)+v1c(k,1)) * e2
       !!
       !! h contains D(rho*Exc)/D(|grad rho|) * (grad rho) / |grad rho|
       !h(:,k,1) = (v2x(k,1)+v2c(1,k,1)) * grho(:,k,1) * e2 
       !!
       !kedtaur(k,1) = (v3x(k,1)+v3c(k,1)) * 0.5d0 * e2
       !!
       !etxc = etxc + (ex(k)+ec(k)) * e2
       !vtxc = vtxc + (v1x(k,1)+v1c(k,1)) * e2 * ABS(rho%of_r(k,1))
       !!
       !IF (rho%of_r(k,1) < zero) rhoneg(1) = rhoneg(1)-rho%of_r(k,1)
       !!
    !ENDDO
    !!
  !ELSE
    !!
    !CALL rhoz_or_updw( rho, 'only_r', '->updw' )
    !!
    !CALL xc_metagcx( dfftp%nnr, 2, np, rho%of_r, grho, rho%kin_r/e2, ex, ec, &
                     !v1x, v2x, v3x, v1c, v2c, v3c )
    !!
    !! first term of the gradient correction : D(rho*Exc)/D(rho)
    !!
    !DO k = 1, dfftp%nnr
       !!
       !v(k,1) = (v1x(k,1) + v1c(k,1)) * e2
       !v(k,2) = (v1x(k,2) + v1c(k,2)) * e2
       !!
       !! h contains D(rho*Exc)/D(|grad rho|) * (grad rho) / |grad rho|
       !!
       !h(:,k,1) = (v2x(k,1) * grho(:,k,1) + v2c(:,k,1)) * e2                     !^^1
       !h(:,k,2) = (v2x(k,2) * grho(:,k,2) + v2c(:,k,2)) * e2
       !!
       !kedtaur(k,1) = (v3x(k,1) + v3c(k,1)) * 0.5d0 * e2
       !kedtaur(k,2) = (v3x(k,2) + v3c(k,2)) * 0.5d0 * e2
       !!
       !etxc = etxc + (ex(k)+ec(k)) * e2
       !vtxc = vtxc + (v1x(k,1)+v1c(k,1)) * ABS(rho%of_r(k,1)) * e2
       !vtxc = vtxc + (v1x(k,2)+v1c(k,2)) * ABS(rho%of_r(k,2)) * e2
       !!
       !IF ( rho%of_r(k,1) < 0.d0 ) rhoneg(1) = rhoneg(1) - rho%of_r(k,1)
       !IF ( rho%of_r(k,2) < 0.d0 ) rhoneg(2) = rhoneg(2) - rho%of_r(k,2)
       !!
    !ENDDO
    !!
    !CALL rhoz_or_updw( rho, 'only_r', '->rhoz' )
    !!
  !ENDIF
  !!
  !DEALLOCATE( ex, ec )
  !DEALLOCATE( v1x, v2x, v3x )
  !DEALLOCATE( v1c, v2c, v3c )
  !!
  !!
  !ALLOCATE( dh( dfftp%nnr ) )    
  !!
  !! ... second term of the gradient correction :
  !! ... \sum_alpha (D / D r_alpha) ( D(rho*Exc)/D(grad_alpha rho) )
  !!
  !ALLOCATE (rhoout(dfftp%nnr))
  !DO is = 1, nspin
     !!
     !CALL fft_graddot( dfftp, h(1,1,is), g, dh )
     !!
     !v(:,is) = v(:,is) - dh(:)
     !!
     !! ... rhoout is in (up,down) format 
     !!
     !rhoout(:) = ( rho%of_r(:,1) + sgn(is)*rho%of_r(:,nspin) )*0.5D0
     !vtxc = vtxc - SUM( dh(:) * rhoout(:) )
     !!
  !END DO
  !DEALLOCATE(rhoout)
  !DEALLOCATE(dh)
  !!
  !CALL mp_sum( rhoneg, intra_bgrp_comm )
  !!
  !rhoneg(:) = rhoneg(:) * omega / ( dfftp%nr1*dfftp%nr2*dfftp%nr3 )
  !!
  !IF ((rhoneg(1) > eps8) .OR. (rhoneg(2) > eps8)) THEN
    !write (stdout, '(/,5x, "negative rho (up,down): ", 2es10.3)') rhoneg(:)
  !ENDIF
  !!
  !vtxc = omega * vtxc / ( dfftp%nr1*dfftp%nr2*dfftp%nr3 ) 
  !etxc = omega * etxc / ( dfftp%nr1*dfftp%nr2*dfftp%nr3 )
  !!
  !IF ( dft_is_nonlocc() ) CALL nlc( rho%of_r, rho_core, nspin, etxc, vtxc, v )
  !!
  !CALL mp_sum(  vtxc , intra_bgrp_comm )
  !CALL mp_sum(  etxc , intra_bgrp_comm )
  !!
  !DEALLOCATE(grho)
  !DEALLOCATE(h)
  !!
  !CALL stop_clock( 'v_xc_meta' )
  !!
  !RETURN
  !!
!END SUBROUTINE v_xc_meta
!!
!!
!SUBROUTINE v_xc( rho, rho_core, rhog_core, etxc, vtxc, v )
  !!----------------------------------------------------------------------------
  !!! Exchange-Correlation potential Vxc(r) from n(r)
  !!
  !USE kinds,            ONLY : DP
  !USE constants,        ONLY : e2, eps8
  !USE io_global,        ONLY : stdout
  !USE fft_base,         ONLY : dfftp
  !USE gvect,            ONLY : ngm
  !USE lsda_mod,         ONLY : nspin
  !USE cell_base,        ONLY : omega
  !USE spin_orb,         ONLY : domag
  !USE funct,            ONLY : nlc, dft_is_nonlocc
  !USE xc_lda_lsda,      ONLY : xc
  !USE scf,              ONLY : scf_type
  !USE mp_bands,         ONLY : intra_bgrp_comm
  !USE mp,               ONLY : mp_sum
  !!
  !IMPLICIT NONE
  !!
  !TYPE (scf_type), INTENT(INOUT) :: rho
  !!! the valence charge
  !REAL(DP), INTENT(IN) :: rho_core(dfftp%nnr)
  !!! the core charge
  !COMPLEX(DP), INTENT(IN) :: rhog_core(ngm)
  !!! the core charge in reciprocal space
  !REAL(DP), INTENT(OUT) :: v(dfftp%nnr,nspin)
  !!! V_xc potential
  !REAL(DP), INTENT(OUT) :: vtxc
  !!! integral V_xc * rho
  !REAL(DP), INTENT(OUT) :: etxc
  !!! E_xc energy
  !!
  !! ... local variables
  !!
  !REAL(DP) :: rhoneg(2), vs
  !!
  !!REAL(DP), ALLOCATABLE :: arhox(:), amag(:), zeta(:)
  !REAL(DP) :: arho, amag
  !REAL(DP) :: rhoup2, rhodw2
  !REAL(DP), ALLOCATABLE :: ex(:), ec(:)
  !REAL(DP), ALLOCATABLE :: vx(:,:), vc(:,:)
  !! In order:
    !! the absolute value of the total charge
    !! the absolute value of the magnetization
    !! zeta = amag / arhox
    !! local exchange energy
    !! local correlation energy
    !! local exchange potential
    !! local correlation potential
  !INTEGER :: ir, ipol
    !! counter on mesh points
    !! counter on nspin
  !!
  !REAL(DP), PARAMETER :: vanishing_charge = 1.D-10, &
                         !vanishing_mag    = 1.D-20
  !!
  !!
  !CALL start_clock( 'v_xc' )
  !!
  !ALLOCATE( ex(dfftp%nnr) )
  !ALLOCATE( ec(dfftp%nnr) )
  !ALLOCATE( vx(dfftp%nnr,nspin) )
  !ALLOCATE( vc(dfftp%nnr,nspin) )
  !!
  !etxc   = 0.D0
  !vtxc   = 0.D0
  !v(:,:) = 0.D0
  !rhoneg = 0.D0
  !!
  !!
  !rho%of_r(:,1) = rho%of_r(:,1) + rho_core(:)
  !!
  !IF ( nspin == 1 .OR. ( nspin == 4 .AND. .NOT. domag ) ) THEN
     !! ... spin-unpolarized case
     !!
     !CALL xc( dfftp%nnr, 1, 1, rho%of_r(:,1), ex, ec, vx(:,1), vc(:,1) )
     !!
     !DO ir = 1, dfftp%nnr
        !v(ir,1) = e2*( vx(ir,1) + vc(ir,1) )
        !etxc = etxc + e2*( ex(ir) + ec(ir) )*rho%of_r(ir,1)
        !rho%of_r(ir,1) = rho%of_r(ir,1) - rho_core(ir)
        !vtxc = vtxc + v(ir,1)*rho%of_r(ir,1)
        !IF (rho%of_r(ir,1) < 0.D0) rhoneg(1) = rhoneg(1)-rho%of_r(ir,1)
     !ENDDO
     !!
     !!
  !ELSEIF ( nspin == 2 ) THEN
     !! ... spin-polarized case
     !!
     !CALL xc( dfftp%nnr, 2, 2, rho%of_r, ex, ec, vx, vc )
     !!
     !DO ir = 1, dfftp%nnr   !OMP ?
        !v(ir,:) = e2*( vx(ir,:) + vc(ir,:) )
        !etxc = etxc + e2*( (ex(ir) + ec(ir))*rho%of_r(ir,1) )
        !rho%of_r(ir,1) = rho%of_r(ir,1) - rho_core(ir)
        !vtxc = vtxc + ( ( v(ir,1) + v(ir,2) )*rho%of_r(ir,1) + &
                        !( v(ir,1) - v(ir,2) )*rho%of_r(ir,2) )
        !!
        !rhoup2 = rho%of_r(ir,1)+rho%of_r(ir,2)
        !rhodw2 = rho%of_r(ir,1)-rho%of_r(ir,2)
        !IF (rhoup2 < 0.d0) rhoneg(1) = rhoneg(1) + rhoup2
        !IF (rhodw2 < 0.d0) rhoneg(2) = rhoneg(2) + rhodw2
     !ENDDO
     !!
     !vtxc   = 0.5d0 * vtxc
     !rhoneg = 0.5d0 * rhoneg
     !!
     !!
  !ELSE IF ( nspin == 4 ) THEN
     !! ... noncolinear case
     !!
     !CALL xc( dfftp%nnr, 4, 2, rho%of_r, ex, ec, vx, vc )
     !!
     !DO ir = 1, dfftp%nnr  !OMP ?
        !arho = ABS( rho%of_r(ir,1) )
        !IF ( arho < vanishing_charge ) CYCLE
        !vs = 0.5D0*( vx(ir,1) + vc(ir,1) - vx(ir,2) - vc(ir,2) )
        !v(ir,1) = e2*( 0.5D0*( vx(ir,1) + vc(ir,1) + vx(ir,2) + vc(ir,2) ) )
        !!
        !amag = SQRT( SUM( rho%of_r(ir,2:4)**2 ) )
        !IF ( amag > vanishing_mag ) THEN
           !v(ir,2:4) = e2 * vs * rho%of_r(ir,2:4) / amag
           !vtxc = vtxc + SUM( v(ir,2:4) * rho%of_r(ir,2:4) )
        !ENDIF
        !etxc = etxc + e2*( ex(ir) + ec(ir) ) * arho
        !!
        !rho%of_r(ir,1) = rho%of_r(ir,1) - rho_core(ir)
        !IF ( rho%of_r(ir,1) < 0.D0 )  rhoneg(1) = rhoneg(1) - rho%of_r(ir,1)
        !IF ( amag / arho > 1.D0 )  rhoneg(2) = rhoneg(2) + 1.D0/omega
        !vtxc = vtxc + v(ir,1) * rho%of_r(ir,1)
     !ENDDO
     !!
     !!
  !ENDIF
  !!
  !DEALLOCATE( ex, ec )
  !DEALLOCATE( vx, vc )
  !!
  !CALL mp_sum(  rhoneg , intra_bgrp_comm )
  !!
  !rhoneg(:) = rhoneg(:) * omega / ( dfftp%nr1*dfftp%nr2*dfftp%nr3 )
  !!
  !IF ( rhoneg(1) > eps8 .OR. rhoneg(2) > eps8 ) &
     !WRITE( stdout,'(/,5X,"negative rho (up, down): ",2ES10.3)') rhoneg
  !!
  !! ... energy terms, local-density contribution
  !!
  !vtxc = omega * vtxc / ( dfftp%nr1*dfftp%nr2*dfftp%nr3 )
  !etxc = omega * etxc / ( dfftp%nr1*dfftp%nr2*dfftp%nr3 )
  !!
  !! ... add gradient corrections (if any)
  !!
  !CALL gradcorr( rho%of_r, rho%of_g, rho_core, rhog_core, etxc, vtxc, v )
  !!
  !! ... add non local corrections (if any)
  !!
  !IF ( dft_is_nonlocc() ) CALL nlc( rho%of_r, rho_core, nspin, etxc, vtxc, v )
  !!
  !CALL mp_sum(  vtxc , intra_bgrp_comm )
  !CALL mp_sum(  etxc , intra_bgrp_comm )
  !!
  !CALL stop_clock( 'v_xc' )
  !!
  !RETURN
  !!
!END SUBROUTINE v_xc
!!
!!----------------------------------------------------------------------------
!SUBROUTINE v_h( rhog, ehart, charge, v )
  !!----------------------------------------------------------------------------
  !!! Hartree potential VH(r) from n(G)
  !!
  !USE constants,         ONLY : fpi, e2
  !USE kinds,             ONLY : DP
  !USE fft_base,          ONLY : dfftp
  !USE fft_interfaces,    ONLY : invfft
  !USE gvect,             ONLY : ngm, gg, gstart
  !USE lsda_mod,          ONLY : nspin
  !USE cell_base,         ONLY : omega, tpiba2
  !USE control_flags,     ONLY : gamma_only
  !USE mp_bands,          ONLY : intra_bgrp_comm
  !USE mp,                ONLY : mp_sum
  !USE martyna_tuckerman, ONLY : wg_corr_h, do_comp_mt
  !USE esm,               ONLY : do_comp_esm, esm_hartree, esm_bc
  !USE Coul_cut_2D,       ONLY : do_cutoff_2D, cutoff_2D, cutoff_hartree  
  !!
  !IMPLICIT NONE
  !!
  !COMPLEX(DP), INTENT(IN) :: rhog(ngm)
  !!! the charge density in reciprocal space
  !REAL(DP), INTENT(INOUT) :: v(dfftp%nnr,nspin)
  !!! Hartree potential
  !REAL(DP), INTENT(OUT) :: ehart
  !!! Hartree energy
  !REAL(DP), INTENT(OUT) :: charge
  !!
  !!  ... local variables
  !!
  !REAL(DP)              :: fac
  !REAL(DP), ALLOCATABLE :: aux1(:,:)
  !REAL(DP)              :: rgtot_re, rgtot_im, eh_corr
  !INTEGER               :: is, ig
  !COMPLEX(DP), ALLOCATABLE :: aux(:), rgtot(:), vaux(:)
  !INTEGER               :: nt
  !!
  !CALL start_clock( 'v_h' )
  !!
  !ALLOCATE( aux( dfftp%nnr ), aux1( 2, ngm ) )
  !charge = 0.D0
  !!
  !IF ( gstart == 2 ) THEN
     !!
     !charge = omega*REAL( rhog(1) )
     !!
  !END IF
  !!
  !CALL mp_sum(  charge , intra_bgrp_comm )
  !!
  !! ... calculate hartree potential in G-space (NB: V(G=0)=0 )
  !!
  !IF ( do_comp_esm .and. ( esm_bc .ne. 'pbc' ) ) THEN
     !!
     !! ... calculate modified Hartree potential for ESM
     !!
     !CALL esm_hartree (rhog, ehart, aux)
     !!
  !ELSE
     !!
     !ehart     = 0.D0
     !aux1(:,:) = 0.D0
     !!
     !IF (do_cutoff_2D) THEN  !TS
        !CALL cutoff_hartree(rhog(:), aux1, ehart)
     !ELSE
!!$omp parallel do private( fac, rgtot_re, rgtot_im ), reduction(+:ehart)
        !DO ig = gstart, ngm
           !!
           !fac = 1.D0 / gg(ig) 
           !!
           !rgtot_re = REAL(  rhog(ig) )
           !rgtot_im = AIMAG( rhog(ig) )
           !!
           !ehart = ehart + ( rgtot_re**2 + rgtot_im**2 ) * fac
           !!
           !aux1(1,ig) = rgtot_re * fac
           !aux1(2,ig) = rgtot_im * fac
           !!
        !ENDDO
!!$omp end parallel do
     !ENDIF
     !!
     !fac = e2 * fpi / tpiba2
     !!
     !ehart = ehart * fac
     !!
     !aux1 = aux1 * fac
     !!
     !IF ( gamma_only ) THEN
        !!
        !ehart = ehart * omega
        !!
     !ELSE 
        !!
        !ehart = ehart * 0.5D0 * omega
        !!
     !END IF
     !! 
     !if (do_comp_mt) then
        !ALLOCATE( vaux( ngm ), rgtot(ngm) )
        !rgtot(:) = rhog(:)
        !CALL wg_corr_h (omega, ngm, rgtot, vaux, eh_corr)
        !aux1(1,1:ngm) = aux1(1,1:ngm) + REAL( vaux(1:ngm))
        !aux1(2,1:ngm) = aux1(2,1:ngm) + AIMAG(vaux(1:ngm))
        !ehart = ehart + eh_corr
        !DEALLOCATE( rgtot, vaux )
     !end if
     !!
     !CALL mp_sum(  ehart , intra_bgrp_comm )
     !! 
     !aux(:) = 0.D0
     !!
     !aux(dfftp%nl(1:ngm)) = CMPLX( aux1(1,1:ngm), aux1(2,1:ngm), KIND=dp )
     !!
     !IF ( gamma_only ) THEN
        !!
        !aux(dfftp%nlm(1:ngm)) = CMPLX( aux1(1,1:ngm), -aux1(2,1:ngm), KIND=dp )
        !!
     !END IF
  !END IF
  !!
  !! ... transform hartree potential to real space
  !!
  !CALL invfft('Rho', aux, dfftp)
  !!
  !! ... add hartree potential to the xc potential
  !!
  !IF ( nspin == 4 ) THEN
     !!
     !v(:,1) = v(:,1) + DBLE(aux(:))
     !!
  !ELSE
     !!
     !DO is = 1, nspin
        !!
        !v(:,is) = v(:,is) + DBLE(aux(:))
        !!
     !END DO
     !!
  !END IF
  !!
  !DEALLOCATE( aux, aux1 )
  !!
  !CALL stop_clock( 'v_h' )
  !!
  !RETURN
  !!
!END SUBROUTINE v_h
!!
!!-----------------------------------------------------------------------
!SUBROUTINE v_hubbard( ns, v_hub, eth )
  !!---------------------------------------------------------------------
  !!! Computes Hubbard potential and Hubbard energy
  !!
  !USE kinds,                ONLY : DP
  !USE ions_base,            ONLY : nat, ityp
  !USE ldaU,                 ONLY : Hubbard_lmax, Hubbard_l, Hubbard_U, &
                                   !Hubbard_J, Hubbard_alpha, lda_plus_u_kind,&
                                   !Hubbard_J0, Hubbard_beta
  !USE lsda_mod,             ONLY : nspin
  !USE control_flags,        ONLY : iverbosity
  !USE io_global,            ONLY : stdout
  !!
  !IMPLICIT NONE
  !!
  !REAL(DP), INTENT(IN)  :: ns(2*Hubbard_lmax+1,2*Hubbard_lmax+1,nspin,nat)
  !!! Occupation matrix
  !REAL(DP), INTENT(OUT) :: v_hub(2*Hubbard_lmax+1,2*Hubbard_lmax+1,nspin,nat)
  !!! Hubbard potential
  !REAL(DP), INTENT(OUT) :: eth
  !!! Hubbard energy
  !!
  !!  ... local variables
  !!
  !REAL(DP) :: n_tot, n_spin, eth_dc, eth_u, mag2, effU, sgn(2) 
  !INTEGER  :: is, isop, is1, na, nt, m1, m2, m3, m4
  !REAL(DP), ALLOCATABLE :: u_matrix(:,:,:,:)
  !!
  !ALLOCATE( u_matrix(2*Hubbard_lmax+1, 2*Hubbard_lmax+1, 2*Hubbard_lmax+1, 2*Hubbard_lmax+1) )
  !!
  !eth    = 0.d0
  !eth_dc = 0.d0
  !eth_u  = 0.d0
  !!
  !sgn(1)=1.d0  ;   sgn(2)=-1.d0
  !!
  !v_hub(:,:,:,:) = 0.d0
  !!
  !IF (lda_plus_u_kind==0) THEN
    !!
    !DO na = 1, nat
       !nt = ityp (na)
       !IF (Hubbard_U(nt) /= 0.d0 .OR. Hubbard_alpha(nt) /= 0.d0) THEN
          !IF (Hubbard_J0(nt) /= 0.d0) THEN
             !effU = Hubbard_U(nt) - Hubbard_J0(nt)
          !ELSE
             !effU = Hubbard_U(nt)
          !END IF  
          !DO is = 1, nspin
             !DO m1 = 1, 2 * Hubbard_l(nt) + 1
                !eth = eth + ( Hubbard_alpha(nt) + 0.5D0*effU )*ns(m1,m1,is,na)
                !v_hub(m1,m1,is,na) = v_hub(m1,m1,is,na) + &
                                     !Hubbard_alpha(nt)  + 0.5D0*effU
                !DO m2 = 1, 2 * Hubbard_l(nt) + 1
                   !eth = eth - 0.5D0 * effU * ns(m2,m1,is,na)* ns(m1,m2,is,na)
                   !v_hub(m1,m2,is,na) = v_hub(m1,m2,is,na) - &
                                        !effU * ns(m2,m1,is,na)
                !ENDDO
             !ENDDO
          !ENDDO
       !ENDIF
       !!
       !IF (Hubbard_J0(nt) /= 0.d0 .OR. Hubbard_beta(nt) /= 0.d0) THEN
          !DO is=1, nspin
             !isop = 1
             !IF ( nspin == 2 .AND. is == 1) isop = 2
             !DO m1 = 1, 2 * Hubbard_l(nt) + 1
                !eth = eth + sgn(is)*Hubbard_beta(nt) * ns(m1,m1,is,na)
                !v_hub(m1,m1,is,na) = v_hub(m1,m1,is,na) + sgn(is)*Hubbard_beta(nt)
                !DO m2 = 1, 2*Hubbard_l(nt)+1
                   !eth = eth + 0.5D0*Hubbard_J0(nt)*ns(m2,m1,is,na)*ns(m1,m2,isop,na)
                   !v_hub(m1,m2,is,na) = v_hub(m1,m2,is,na) + Hubbard_J0(nt) * &
                                                             !ns(m2,m1,isop,na)
                !END DO
             !END DO
          !END DO
       !END IF
        
    !END DO
    !!
    !IF (nspin==1) eth = 2.d0 * eth
    !!
!!-- output of hubbard energies:
    !IF ( iverbosity > 0 ) THEN
      !write(stdout,*) '--- in v_hubbard ---'
      !write(stdout,'("Hubbard energy ",f9.4)') eth
      !write(stdout,*) '-------'
    !ENDIF
!!--
    !!
  !ELSE
    !!
    !DO na = 1, nat
       !nt = ityp (na)
       !IF (Hubbard_U(nt)/=0.d0) THEN
          !!
!!       initialize U(m1,m2,m3,m4) matrix 
          !CALL hubbard_matrix( Hubbard_lmax, Hubbard_l(nt), Hubbard_U(nt), &
                               !Hubbard_J(1,nt), u_matrix )
          !!
!!---      total N and M^2 for DC (double counting) term
          !n_tot = 0.d0
          !DO is = 1, nspin
            !DO m1 = 1, 2 * Hubbard_l(nt) + 1
              !n_tot = n_tot + ns(m1,m1,is,na)
            !ENDDO
          !ENDDO
          !IF (nspin==1) n_tot = 2.d0 * n_tot
          !!
          !mag2  = 0.d0
          !IF (nspin==2) THEN
            !DO m1 = 1, 2 * Hubbard_l(nt) + 1
              !mag2 = mag2 + ns(m1,m1,1,na) - ns(m1,m1,2,na)
            !ENDDO
          !ENDIF
          !mag2  = mag2**2
!!---

!!---      hubbard energy: DC term

          !eth_dc = eth_dc + 0.5d0*( Hubbard_U(nt)*n_tot*(n_tot-1.d0) - &
                                    !Hubbard_J(1,nt)*n_tot*(0.5d0*n_tot-1.d0) - &
                                    !0.5d0*Hubbard_J(1,nt)*mag2 )
!!--
          !DO is = 1, nspin
            !!
!!---        n_spin = up/down N

            !n_spin = 0.d0
            !DO m1 = 1, 2 * Hubbard_l(nt) + 1
               !n_spin = n_spin + ns(m1,m1,is,na)
            !ENDDO
!!---

            !DO m1 = 1, 2 * Hubbard_l(nt) + 1

!!             hubbard potential: DC contribution  

              !v_hub(m1,m1,is,na) = v_hub(m1,m1,is,na) + Hubbard_J(1,nt)*n_spin + &
                      !0.5d0*(Hubbard_U(nt)-Hubbard_J(1,nt)) - Hubbard_U(nt)*n_tot

!!             +U contributions 

              !DO m2 = 1, 2 * Hubbard_l(nt) + 1
                !DO m3 = 1, 2 * Hubbard_l(nt) + 1
                  !DO m4 = 1, 2 * Hubbard_l(nt) + 1

                    !DO is1 = 1, nspin
                       !v_hub(m1,m2,is,na) = v_hub(m1,m2,is,na) + (MOD(nspin,2)+1) * &
                                         !u_matrix(m1,m3,m2,m4) * ns(m3,m4,is1,na)
                    !ENDDO
                    !!
                    !v_hub(m1,m2,is,na) = v_hub(m1,m2,is,na) - &
                                      !u_matrix(m1,m3,m4,m2) * ns(m3,m4,is,na)
                    !!
                    !eth_u = eth_u + 0.5d0*( ( u_matrix(m1,m2,m3,m4)-u_matrix(m1,m2,m4,m3) ) * &
                                    !ns(m1,m3,is,na)*ns(m2,m4,is,na)+u_matrix(m1,m2,m3,m4)   * &
                                    !ns(m1,m3,is,na)*ns(m2,m4,nspin+1-is,na) )
                  !ENDDO
                !ENDDO
              !ENDDO
            !ENDDO
            !!
          !ENDDO
          !!
       !ENDIF
    !ENDDO
    !!
    !IF (nspin==1) eth_u = 2.d0 * eth_u
    !eth = eth_u - eth_dc

!!-- output of hubbard energies:
    !IF ( iverbosity > 0 ) THEN
      !write(stdout,*) '--- in v_hubbard ---'
      !write(stdout,'("Hubbard energies (dc, U, total) ",3f9.4)') eth_dc, eth_u, eth
      !write(stdout,*) '-------'
    !ENDIF
!!--

  !ENDIF

  !DEALLOCATE (u_matrix)
  !RETURN

!END SUBROUTINE v_hubbard
!!-------------------------------------

!SUBROUTINE v_hubbard_nc( ns, v_hub, eth )
  !!-------------------------------------
  !!! Noncollinear version of v_hubbard.
  !!
  !USE kinds,                ONLY : DP
  !USE ions_base,            ONLY : nat, ityp
  !USE ldaU,                 ONLY : Hubbard_lmax, Hubbard_l, &
                                   !Hubbard_U, Hubbard_J, Hubbard_alpha
  !USE lsda_mod,             ONLY : nspin
  !USE control_flags,        ONLY : iverbosity
  !USE io_global,            ONLY : stdout
  !!
  !IMPLICIT NONE
  !!
  !COMPLEX(DP) :: ns(2*Hubbard_lmax+1,2*Hubbard_lmax+1,nspin,nat)
  !!! Occupation matrix
  !COMPLEX(DP) :: v_hub(2*Hubbard_lmax+1,2*Hubbard_lmax+1,nspin,nat)
  !!! Hubbard potential
  !REAL(DP) :: eth
  !!! Hubbard matrix
  !!
  !!  ... local variables
  !!
  !REAL(DP) :: eth_dc, eth_noflip, eth_flip, psum, mx, my, mz, mag2
  !INTEGER :: is, is1, js, i, j, na, nt, m1, m2, m3, m4
  !COMPLEX(DP) :: n_tot, n_aux
  !REAL(DP), ALLOCATABLE :: u_matrix(:,:,:,:)
  !!
  !ALLOCATE( u_matrix(2*Hubbard_lmax+1, 2*Hubbard_lmax+1, 2*Hubbard_lmax+1, 2*Hubbard_lmax+1) )
  !!
  !eth        = 0.d0
  !eth_dc     = 0.d0  
  !eth_noflip = 0.d0  
  !eth_flip   = 0.d0  
  !!
  !v_hub(:,:,:,:) = 0.d0
  !!
  !DO na = 1, nat  
     !nt = ityp (na)  
     !IF (Hubbard_U(nt) /= 0.d0) THEN  

!!       !initialize U(m1,m2,m3,m4) matrix 
        !CALL hubbard_matrix( Hubbard_lmax, Hubbard_l(nt), Hubbard_U(nt), &
                             !Hubbard_J(1,nt), u_matrix )

!!---    !total N and M^2 for DC (double counting) term
        !n_tot = 0.d0
        !mx    = 0.d0
        !my    = 0.d0
        !mz    = 0.d0
        !DO m1 = 1, 2*Hubbard_l(nt)+1
          !n_tot = n_tot + ns(m1,m1,1,na) + ns(m1,m1,4,na)
          !mx = mx + DBLE( ns(m1, m1, 2, na) + ns(m1, m1, 3, na) )
          !my = my + 2.d0 * AIMAG( ns(m1, m1, 2, na) )
          !mz = mz + DBLE( ns(m1, m1, 1, na) - ns(m1, m1, 4, na) )
        !ENDDO  
        !mag2 = mx**2 + my**2 + mz**2  
!!---

!!---    !hubbard energy: DC term
        !mx = REAL(n_tot)
        !eth_dc = eth_dc + 0.5d0*( Hubbard_U(nt)*mx*(mx-1.d0) - &
                                  !Hubbard_J(1,nt)*mx*(0.5d0*mx-1.d0) - &
                                  !0.5d0*Hubbard_J(1,nt)*mag2 )   
!!--
        !DO is = 1, nspin  
           !IF (is == 2) THEN
            !is1 = 3
           !ELSEIF (is == 3) THEN
            !is1 = 2
           !ELSE
            !is1 = is
           !ENDIF

!!---       !hubbard energy:
           !IF (is1 == is) THEN
!!--         !non spin-flip contribution
            !DO m1 = 1, 2*Hubbard_l(nt)+1
             !DO m2 = 1, 2*Hubbard_l(nt)+1
               !DO m3 = 1, 2*Hubbard_l(nt)+1
                !DO m4 = 1, 2*Hubbard_l(nt)+1
                  !!
                  !eth_noflip = eth_noflip + 0.5d0*(                            &
                             !( u_matrix(m1,m2,m3,m4)-u_matrix(m1,m2,m4,m3) )*  & 
                             !ns(m1,m3,is,na)*ns(m2,m4,is,na) +                 &
                     !u_matrix(m1,m2,m3,m4)*ns(m1,m3,is,na)*ns(m2,m4,nspin+1-is,na) )
                  !!
                !ENDDO
               !ENDDO
              !ENDDO
             !ENDDO
             !!
           !ELSE
!!--         !spin-flip contribution
            !DO m1 = 1, 2*Hubbard_l(nt)+1
             !DO m2 = 1, 2*Hubbard_l(nt)+1
               !DO m3 = 1, 2*Hubbard_l(nt)+1
                !DO m4 = 1, 2*Hubbard_l(nt)+1
                  !!
                  !eth_flip = eth_flip - 0.5d0*u_matrix(m1,m2,m4,m3)* &
                                    !ns(m1,m3,is,na)*ns(m2,m4,is1,na) 
                  !!
                !ENDDO
               !ENDDO
              !ENDDO
             !ENDDO
             !!
           !ENDIF
!!---

!!---       !hubbard potential: non spin-flip contribution 
           !IF (is1 == is) THEN
            !DO m1 = 1, 2*Hubbard_l(nt)+1
             !DO m2 = 1, 2*Hubbard_l(nt)+1

               !DO m3 = 1, 2*Hubbard_l(nt)+1
                !DO m4 = 1, 2*Hubbard_l(nt)+1
                  !v_hub(m1,m2,is,na) = v_hub(m1,m2,is,na) + &
                    !u_matrix(m1,m3,m2,m4)*( ns(m3,m4,1,na)+ns(m3,m4,4,na) ) 
                !ENDDO 
               !ENDDO
               !!
              !ENDDO
             !ENDDO
           !ENDIF
!!---
            
!!---       !n_aux = /sum_{i} n_{i,i}^{sigma2, sigma1} for DC term
           !n_aux = 0.d0
           !DO m1 = 1, 2*Hubbard_l(nt)+1
              !n_aux = n_aux + ns(m1,m1,is1,na)  
           !ENDDO
!!---

           !DO m1 = 1, 2*Hubbard_l(nt)+1
           
!!---          !hubbard potential: DC contribution  
              !v_hub(m1,m1,is,na) = v_hub(m1,m1,is,na) + Hubbard_J(1,nt)*n_aux
              !IF (is1 == is) THEN
                 !v_hub(m1,m1,is,na) = v_hub(m1,m1,is,na) + &
                 !0.5d0*(Hubbard_U(nt)-Hubbard_J(1,nt)) - Hubbard_U(nt)*n_tot  
              !ENDIF
!!---
              
!!---          !hubbard potential: spin-flip contribution
              !DO m2 = 1, 2*Hubbard_l(nt)+1  
                !!
                !DO m3 = 1, 2*Hubbard_l(nt)+1
                  !DO m4 = 1, 2*Hubbard_l(nt)+1
                          !v_hub(m1,m2,is,na) = v_hub(m1,m2,is,na) - &
                                    !u_matrix(m1,m3,m4,m2) * ns(m3,m4,is1,na) 
                  !ENDDO 
                !ENDDO

              !ENDDO
!!---
           !ENDDO
        !ENDDO

     !ENDIF
  !ENDDO

  !eth = eth_noflip + eth_flip - eth_dc

!!-- output of hubbard energies:
  !IF ( iverbosity > 0 ) THEN
    !write(stdout,*) '--- in v_hubbard ---'
    !write(stdout,'("Hub. E (dc, noflip, flip, total) ",4f9.4)') &
                                 !eth_dc, eth_noflip, eth_flip, eth 
    !write(stdout,*) '-------'
  !ENDIF
!!--

  !DEALLOCATE (u_matrix)
  !RETURN
!END SUBROUTINE v_hubbard_nc
!!-------------------------------------------

!!----------------------------------------------------------------------------
!SUBROUTINE v_h_of_rho_r( rhor, ehart, charge, v )
  !!----------------------------------------------------------------------------
  !!! Hartree potential VH(r) from a density in R space n(r) 
  !!
  !USE kinds,           ONLY : DP
  !USE fft_base,        ONLY : dfftp
  !USE fft_interfaces,  ONLY : fwfft
  !USE lsda_mod,        ONLY : nspin
  !!
  !IMPLICIT NONE
  !!
  !! ... Declares variables
  !!
  !REAL( DP ), INTENT(IN)     :: rhor( dfftp%nnr )
  !REAL( DP ), INTENT(INOUT)  :: v( dfftp%nnr )
  !REAL( DP ), INTENT(OUT)    :: ehart, charge
  !!
  !! ... Local variables
  !!
  !COMPLEX( DP ), ALLOCATABLE :: rhog( : )
  !COMPLEX( DP ), ALLOCATABLE :: aux( : )
  !REAL( DP ), ALLOCATABLE :: vaux(:,:)
  !INTEGER :: is
  !!
  !! ... bring the (unsymmetrized) rho(r) to G-space (use aux as work array)
  !!
  !ALLOCATE( rhog( dfftp%ngm ) )
  !ALLOCATE( aux( dfftp%nnr ) )
  !aux = CMPLX(rhor,0.D0,kind=dp)
  !CALL fwfft ('Rho', aux, dfftp)
  !rhog(:) = aux(dfftp%nl(:))
  !DEALLOCATE( aux )
  !!
  !! ... compute VH(r) from n(G)
  !!
  !ALLOCATE( vaux( dfftp%nnr, nspin ) )
  !vaux = 0.D0
  !CALL v_h( rhog, ehart, charge, vaux )
  !v(:) = v(:) + vaux(:,1)
  !!
  !DEALLOCATE( rhog )
  !DEALLOCATE( vaux )
  !!
  !RETURN
  !!
!END SUBROUTINE v_h_of_rho_r
!!----------------------------------------------------------------------------
!SUBROUTINE gradv_h_of_rho_r( rho, gradv )
  !!----------------------------------------------------------------------------
  !!! Gradient of Hartree potential in R space from a total 
  !!! (spinless) density in R space n(r)
  !!
  !USE kinds,           ONLY : DP
  !USE fft_base,        ONLY : dfftp
  !USE fft_interfaces,  ONLY : fwfft, invfft
  !USE constants,       ONLY : fpi, e2
  !USE control_flags,   ONLY : gamma_only
  !USE cell_base,       ONLY : tpiba, omega
  !USE gvect,           ONLY : ngm, gg, gstart, g
  !USE martyna_tuckerman, ONLY : wg_corr_h, do_comp_mt
  !!
  !IMPLICIT NONE
  !!
  !! ... Declares variables
  !!
  !REAL( DP ), INTENT(IN)     :: rho(dfftp%nnr)
  !REAL( DP ), INTENT(OUT)    :: gradv(3, dfftp%nnr)
  !!
  !! ... Local variables
  !!
  !COMPLEX( DP ), ALLOCATABLE :: rhoaux(:)
  !COMPLEX( DP ), ALLOCATABLE :: gaux(:)
  !COMPLEX( DP ), ALLOCATABLE :: rgtot(:), vaux(:)
  !REAL( DP )                 :: fac, eh_corr
  !INTEGER                    :: ig, ipol
  !!
  !! ... Bring rho to G space
  !!
  !ALLOCATE( rhoaux( dfftp%nnr ) )
  !rhoaux( : ) = CMPLX( rho( : ), 0.D0, KIND=dp ) 
  !!
  !CALL fwfft( 'Rho', rhoaux, dfftp )
  !!
  !! ... Compute total potential in G space
  !!
  !ALLOCATE( gaux( dfftp%nnr ) )
  !!
  !DO ipol = 1, 3
    !!
    !gaux(:) = (0.0_dp,0.0_dp)
    !!
    !DO ig = gstart, ngm
      !!
      !fac = g(ipol,ig) / gg(ig)
      !gaux(dfftp%nl(ig)) = CMPLX(-AIMAG(rhoaux(dfftp%nl(ig))),REAL(rhoaux(dfftp%nl(ig))),KIND=dp)*fac 
      !!
    !ENDDO
    !!
    !! ...and add the factor e2*fpi/2\pi/a coming from the missing prefactor of 
    !!  V = e2 * fpi divided by the 2\pi/a factor missing in G  
    !!
    !fac = e2 * fpi / tpiba
    !gaux = gaux * fac 
    !!
    !! ...add martyna-tuckerman correction, if needed
    !! 
    !IF (do_comp_mt) THEN
       !ALLOCATE( vaux( ngm ), rgtot(ngm) )
       !rgtot(1:ngm) = rhoaux(dfftp%nl(1:ngm))
       !CALL wg_corr_h( omega, ngm, rgtot, vaux, eh_corr )
       !DO ig = gstart, ngm
         !fac = g(ipol,ig) * tpiba
         !gaux(dfftp%nl(ig)) = gaux(dfftp%nl(ig)) + CMPLX(-AIMAG(vaux(ig)),REAL(vaux(ig)),kind=dp)*fac 
       !END DO
       !DEALLOCATE( rgtot, vaux )
    !ENDIF
    !!
    !IF ( gamma_only ) THEN
      !!
      !gaux(dfftp%nlm(:)) = &
        !CMPLX( REAL( gaux(dfftp%nl(:)) ), -AIMAG( gaux(dfftp%nl(:)) ) ,kind=DP)
       !!
    !END IF
    !!
    !! ... bring back to R-space, (\grad_ipol a)(r) ...
    !!
    !CALL invfft( 'Rho', gaux, dfftp )
    !!
    !gradv(ipol,:) = REAL( gaux(:) )
    !!
  !ENDDO
  !!
  !DEALLOCATE(gaux)
  !!
  !DEALLOCATE(rhoaux)
  !!
  !RETURN
  !!
!END SUBROUTINE gradv_h_of_rho_r
